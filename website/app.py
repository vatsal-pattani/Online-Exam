from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from .users import *
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'img')
app.config['SECRET_KEY'] = "fnvmkalbguipaehf"

if __name__ == '__main__':
    app.run(debug=True)
# This ensures that this app will run only when this file is executed, and not when this file is imported in some other file


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_type = request.args.get('type')
    if log_type not in ["Student", "IC", "Admin"]:
        return render_template("404.html"), 404
    return render_template("login.html", log_type=log_type)


@app.route('/verify/<log_type>', methods=['POST'])
def verify(log_type):
    print("verification started")
    ID = request.form.get('ID')
    passw = request.form.get('passw')
    result = verify_in_db(ID, passw, log_type)

    if not result:
        # redirect back to home page
        return "<h1>Incorrect ID or Password</h1>"

    print("verified")

    session["ID"] = ID  # Storing in session
    session["log_type"] = log_type  # No need to store password
    print(log_type)
    if(log_type == "Student"):
        return redirect(url_for('dashboard'))
    elif(log_type == "IC"):
        return redirect(url_for('IC_dashboard'))
    elif(log_type == "Admin"):
        return "Admin"
    return "Hehe"


@app.route('/reset password')
def reset_passw():
    return "<h1>Reset Password</h1>"


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    ID = session['ID']
    # getCourses is unnecessary function. We can do it just by execute
    courses = getCourses(ID)
    print("session")
    print(session)
    S_name = execute(f'''select S_id,S_Name 
             from Student as temp_s 
             where (S_id = '{ID}');''')[0][1]
    return render_template("dashboard.html", courses=courses, S_name=S_name)


@app.route('/papers', methods=['GET', 'POST'])
def papers():
    subject = request.args.get('subject')
    session['subject'] = subject
    c_id = execute(
        f'''select C_id from course where (title = '{subject}'); ''')
    session['c_id'] = c_id[0][0]
    papers = execute(
        f'''select E_id,duration,exam_time from Exam where (Exam.C_id = '{c_id[0][0]}'); ''')
    return render_template('papers.html', papers=papers, subject=subject)


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    E_id = request.args.get('E_id')
    session['E_id'] = E_id

    # First check if the student has already attempted this paper
    given = execute(
        f''' select exists(select * from result where (result.c_id='{session['c_id']}') and (result.s_id = '{session['ID']}') and (result.e_id='{session['E_id']}'));''')

    total_marks = execute(
        f'''select total_marks from exam where (exam.e_id = '{E_id}') and (exam.c_id = '{session['c_id']}');''')[0][0]
    session['total_marks'] = total_marks
    print("Total Marks:", total_marks)

    if given[0][0] == 1:
        # given is 1 if student has already attempted the paper
        session['given'] = 1
        return redirect(url_for('result'))

    session['given'] = 0  # Student hasn't attampted the paper

    questions = execute(
        f'''select marks, Question, Opt1, Opt2, Opt3, Opt4, Q_id, correct_ans from Questions where (questions.E_id = '{session['E_id']}') and (questions.C_id = '{session['c_id']}'); -- Displays all questions of that test ''')

    return render_template("questions.html", questions=questions, tm=total_marks, duration=request.args.get('duration'))


@app.route('/result', methods=['GET', 'POST'])
def result():
    total_marks = float(session['total_marks'])
    if(session['given'] == 0):

        questions = execute(
            f'''select marks, Question, Opt1, Opt2, Opt3, Opt4, Q_id, correct_ans from Questions where (questions.E_id = '{session['E_id']}') and (questions.C_id = '{session['c_id']}'); -- Displays all questions of that test ''')

        # store all Q_id in a separate list. Will be useful later while calculating marks
        qid_list = []

        # Fetch all correct answers
        correct_ans = []
        for q in questions:
            correct_ans.append(q[-1])
            # Removing correct answers so that we can pass it to webpage of question paper
            q = q[:7]
            qid_list.append(q[6])

        # Fetch all given answers
        f = request.form
        given_ans = []
        for entry in f:
            given_ans.append(f[entry])

        # Calculate obtained marks now.
        obtained_marks = 0
        i = 0
        while(i < len(correct_ans)):
            if(correct_ans[i] == given_ans[i]):
                obtained_marks = obtained_marks+float(questions[i][0])
            i = i+1

        session['obtained_marks'] = obtained_marks

        # We have to save student's response of this paper to database
        # Here we are not saving E_id to db. Hence, if same question(with same Q_id) is added to multiple papers, and the student attempts multiple of those papers, then it will create an issue.
        # But assume that a question belongs to one paper only
        ID = session['ID']

        query = f'''insert into Response(Q_id,S_id,marks,Response)
                        values '''
        null_val = 'NULL'
        i = 0
        for q in qid_list:
            if(given_ans[i] == 'None'):
                query = query + \
                    f"('{q}','{ID}',{questions[i][0]}, {null_val}),"
            else:
                query = query + \
                    f"('{q}','{ID}',{questions[i][0]}, '{given_ans[i]}'),"
            i = i+1
        query = query[:-1]  # Popping last extra comma
        query += ";"  # Adding one semicolon
        execute(query)    # This saves Response in db

        time_taken = request.form.get('tt')
        # Now We have to add these obtined marks to Result table. Keeping time taken as 0 for now
        execute(f'''insert into Result(E_id, C_id, S_id, marks, time_taken)
                    values ('{session['E_id']}','{session['c_id']}','{ID}',{obtained_marks},{time_taken}); ''')

    else:
        # Fetch student's result from database
        result = execute(
            f'''select marks,time_taken from Result where (Result.C_id = '{session['c_id']}') and (Result.S_id = '{session['ID']}') and (Result.E_id = '{session['E_id']}'); ''')

        print("Result from db: ", result)
        obtained_marks = result[0][0]
        time_taken = result[0][1]
        session['obtained_marks'] = obtained_marks
    return render_template("result.html", om=obtained_marks, tm=total_marks, tt=time_taken)


@app.route('/view_response')
def response():

    # Fetch questions from db
    questions = execute(
        f'''select marks, Question, Opt1, Opt2, Opt3, Opt4, Q_id, correct_ans from Questions where (questions.E_id = '{session['E_id']}') and (questions.C_id = '{session['c_id']}'); -- Displays all questions of that test ''')

    # Fetch given_ans from db
    given_ans = execute(f'''select response from response 
                    where response.s_id='{session['ID']}' and response.Q_id in 
                    (select Q_id from Questions where (Questions.E_id='{session['E_id']}') and (Questions.c_id='{session['c_id']}'));''')

    result = execute(
        f'''select time_taken from Result where (Result.C_id = '{session['c_id']}') and (Result.S_id = '{session['ID']}') and (Result.E_id = '{session['E_id']}'); ''')
    time_taken = result[0][0]
    return render_template('view_r.html', questions=questions, given_ans=given_ans, tm=session['total_marks'], om=session['obtained_marks'], zip=zip, range=range, tt=time_taken)


@app.route('/leaderboard')
def leaderboard():
    LeadBoard = execute(
        f'''select S_id,S_name,marks,time_taken 
            from (Result natural join student)
            where (Result.C_id = '{session['c_id']}') and (Result.E_id = '{session['E_id']}') order by Marks desc, time_taken asc;  -- Displays leaderboard for this test ''')
    print(LeadBoard)
    return render_template('Leaderboard.html', lb=LeadBoard, subject=session['subject'], paper=session['E_id'], tm=session['total_marks'], zip=zip, S_id=session['ID'])


@app.route('/Log Out')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/IC_dashboard')
def IC_dashboard():
    # We have ID and log_type at this point
    # Now we have to fetch all info of his course
    print(session['ID'])
    IC_info = execute(f'''select IC_Name,title,C_id 
                    from Course 
                    where (IC_id = '{session['ID']}'); ''')[0]

    course_name = IC_info[1]
    session['subject'] = course_name
    session['c_id'] = IC_info[2]

    papers = execute(
        f'''select E_id,duration,exam_time from Exam where (Exam.C_id = '{session['c_id']}'); ''')

    return render_template("IC_dashboard.html", IC_info=IC_info, papers=papers, subject=course_name)


@app.route('/view_paper')
def view_paper():
    E_id = request.args.get('E_id')
    print(request.args)
    # session['E_id'] = E_id

    print(E_id)
    print(session['c_id'])
    session['E_id'] = E_id
    questions = execute(
        f'''select marks, Question, Opt1, Opt2, Opt3, Opt4, Q_id, correct_ans from Questions where (questions.E_id = '{E_id}') and (questions.C_id = '{session['c_id']}'); -- Displays all questions of that test ''')

    exam_info = execute(f'''select total_marks, duration from Exam
                              where E_id='{E_id}' and C_id='{session['c_id']}' ''')[0]

    session['total_marks'] = exam_info[0]
    return render_template("questions_IC.html", questions=questions, tm=exam_info[0], duration=exam_info[1])


@app.route('/create_paper', methods=['GET', 'POST'])
def create_paper():
    # First we will have to generate new E_id for this c_id, we'll have to refer to db for that
    last_eid = execute(f'''select E_id from exam
                where exam.c_id = '{session['c_id']}'
                order by E_id desc
                limit 1''')[0][0]
    new_eid = "e" + str(int(last_eid[1:]) + 1).zfill(5)   # Creating a new e_id
    session['new_eid'] = new_eid

    return render_template("create_paper.html", session=session)


@app.route('/add_question', methods=['POST'])
def add_question():  # This will add paper to db
    print("We are here!")
    # print(request.form)
    form = request.form
    last_qid = execute(f'''select Q_id from Questions
                order by Q_id desc
                limit 1''')[0][0]
    new_qid = "q" + str(int(last_qid[1:]) + 1).zfill(5)   # Creating a new e_id
    print(new_qid)
    execute(f'''insert into Questions(Q_id,marks,Question,Opt1,Opt2,Opt3,Opt4,correct_ans,E_id,C_id)
                values ('{new_qid}',{int(form['marks'])},'{form['q']}', '{form['A']}','{form['B']}','{form['C']}','{form['D']}','{form['c_ans']}','{session['new_eid']}','{session['c_id']}'); ''')
    return "Question added successfully"


@app.route('/add_exam', methods=['POST'])
def add_exam():
    # print("We're in add exam!")
    print(request.form)
    form = request.form
    execute(f'''insert into Exam(E_id, C_id, duration, exam_time, total_marks)
                values ('{session['new_eid']}','{session['c_id']}','{form['duration']}','{form['timing']}',{int(form['total_marks'])}) ''')
    flash('Paper Added Successfully', 'success')
    return redirect(url_for('IC_dashboard'))


@app.route('/edit_paper/<E_id>')
def edit_paper(E_id):
    print(E_id)
    return "Here you edit the paper"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )
