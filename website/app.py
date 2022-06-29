from flask import Flask, render_template, request, redirect, url_for, session
from .users import *
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


app = Flask(__name__)
app.config['SECRET_KEY'] = "fnvmkalbguipaehf"

if __name__ == '__main__':
    app.run(debug=True)
# This ensures that this app will run only when this file is executed, and not when this file is imported in some other file


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def home():
    print("home")
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_type = request.args.get('type')
    if log_type not in ["Student", "IC", "Admin"]:
        return render_template("404.html"), 404
    return render_template("login.html", log_type=log_type)


@app.route('/verify/<log_type>', methods=['GET', 'POST'])
def verify(log_type):
    print("verification started")
    print(request.form)
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
    return render_template("dashboard.html", courses=courses)


@app.route('/papers', methods=['GET', 'POST'])
def papers():
    subject = request.form.get('subject')
    subject = subject.split(' : ')[0]
    session['subject'] = subject
    c_id = execute(
        f'''select C_id from course where (title = '{subject}'); ''')
    session['c_id'] = c_id[0][0]
    papers = execute(
        f'''select E_id,duration,exam_time from Exam where (Exam.C_id = '{c_id[0][0]}'); ''')
    return render_template('papers.html', papers=papers)


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    E_id = request.form.get('E_id')
    session['E_id'] = E_id
    total_marks = execute(
        f'''select total_marks from exam where (exam.e_id = '{E_id}') and (exam.c_id = '{session['c_id']}');''')[0][0]

    session['total_marks'] = total_marks
    print("Total Marks:", total_marks)
    # First check if the student has already attempted this paper
    given = execute(
        f''' select exists(select * from result where (result.c_id='{session['c_id']}') and (result.s_id = '{session['ID']}') and (result.e_id='{session['E_id']}'));''')

    if given[0][0] == 1:
        # given is 1 if student has already attempted the paper
        session['given'] = 1
        return redirect(url_for('result'))

    session['given'] = 0  # Student hasn't attampted the paper
    questions = execute(f'''select marks, Question, Opt1, Opt2, Opt3, Opt4, Q_id, correct_ans from Questions where (questions.E_id = 'e00001') and (questions.C_id = 'c00001'); -- Displays all questions of that test ''')
    session['questions'] = questions  # This conains everything including correct answers

    # store all Q_id in a separate list. Will be useful later while calculating marks
    qid_list = []
    ans_list = []
    for q in questions:
        ans_list.append(q[-1])
        # Removing correct answers so that we can pass it to webpage of question paper
        q = q[:7]
        qid_list.append(q[6])

    session['qid_list'] = qid_list  # This is list of q_id
    session['ans_list'] = ans_list  # This is list of correct answers

    # We can calculate total marks of exam here. we actually fetched it from database
    # But the snippet below will be useful when IC creates a paper

    # total_marks=0
    # i=0
    # while(i<len(qid_list)):
    #     total_marks=total_marks+float(questions[i][0])
    #     i=i+1
    # session['total_marks']=total_marks

    # Not passing correct ans and Q_id to HTML as they are not needed
    return render_template("questions.html", questions=questions, tm=total_marks)


@app.route('/result', methods=['GET', 'POST'])
def result():
    total_marks = float(session['total_marks'])
    if(session['given'] == 0):
        q_ids = session['qid_list']
        correct_ans = session['ans_list']
        f = request.form
        given_ans = []
        for entry in f:
            given_ans.append(f[entry])
        session['given_ans'] = given_ans
        questions = session['questions']
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

        # for q in q_ids:                 #This seems inefficient as we are making new connection every time
        #     print(given_ans[i])
        #     db=connect()
        #     db.autocommit=True
        #     cur=db.cursor()
        #     if(given_ans[i]=='None'):
        #         cur.execute(
        #             f'''insert into Response(Q_id,S_id,marks,Response)
        #             values ('{q}', '{ID}',{questions[i][0]}, NULL); -- Marks obtained in each question will be provided by python program'''
        #         )
        #     else:
        #         cur.execute(
        #             f'''insert into Response(Q_id,S_id,marks,Response)
        #             values ('{q}', '{ID}',{questions[i][0]}, '{given_ans[i]}'); -- Marks obtained in each question will be provided by python program'''
        #         ) # This gives error when given ans is None
        #     cur.close()
        #     i=i+1

        query = f'''insert into Response(Q_id,S_id,marks,Response)
                        values '''
        null_val = 'NULL'
        i = 0
        for q in q_ids:
            if(given_ans[i] == 'None'):
                query = query + \
                    f"('{q}','{ID}',{questions[i][0]}, {null_val}),"
            else:
                query = query + \
                    f"('{q}','{ID}',{questions[i][0]}, '{given_ans[i]}'),"
            i = i+1
        query = query[:-1]  # Poppinf last extra comma
        query += ";"  # Adding one semicolon
        execute(query)    # This saves Response in db

        # Now We have to add these obtined marks to Result table. Keeping time taken as 0 for now
        execute(f'''insert into Result(E_id, C_id, S_id, marks, time_taken)
                    values ('{session['E_id']}','{session['c_id']}','{ID}',{obtained_marks},0); ''')

    else:
        # Fetch student's result from database
        result = execute(
            f'''select marks,time_taken from Result where (Result.C_id = '{session['c_id']}') and (Result.S_id = '{session['ID']}') and (Result.E_id = '{session['E_id']}'); ''')

        print("Result from db: ", result)
        obtained_marks = result[0][0]
        session['obtained_marks'] = obtained_marks
    return render_template("result.html", om=obtained_marks, tm=total_marks)


@app.route('/view_response')
def response():
    if(session['given'] == 1):

        # Fetch questions from db, because they are not in session
        questions = execute(
            f'''select marks, Question, Opt1, Opt2, Opt3, Opt4, Q_id, correct_ans from Questions where (questions.E_id = '{session['E_id']}') and (questions.C_id = '{session['c_id']}'); -- Displays all questions of that test ''')

        # Fetch given_ans from db, because they are not in session
        given_ans = execute(f'''select response from response 
                        where response.s_id='{session['ID']}' and response.Q_id in 
                        (select Q_id from Questions where (Questions.E_id='{session['E_id']}') and (Questions.c_id='{session['c_id']}'));''')
        print(given_ans)
    else:
        questions = session['questions']
        given_ans = session['given_ans']
    return render_template('view_r.html', questions=questions, given_ans=given_ans, tm=session['total_marks'], om=session['obtained_marks'], zip=zip, range=range)


@app.route('/leaderboard')
def leaderboard():
    LeadBoard = execute(
        f'''select S_id,marks,time_taken from Result where (Result.C_id = '{session['c_id']}') and (Result.E_id = '{session['E_id']}') order by Marks desc, time_taken asc;  -- Displays leaderboard for this test ''')
    print(LeadBoard)
    return render_template('Leaderboard.html', lb=LeadBoard, subject=session['subject'], paper=session['E_id'], tm=session['total_marks'])


@app.route('/Log Out')
def logout():
    session.pop()
    return redirect(url_for('home'))


@app.route('/IC_dashboard')
def IC_dashboard():
    # We have ID and log_type at this point
    # Now we have to fetch all info of his course
    IC_info = execute(f'''select IC_Name,title,C_id 
                    from Course 
                    where (IC_id = 'p00001') and (IC_Password = 'DBS'); ''')[0]

    course_name = IC_info[1]
    session['course'] = course_name
    papers = execute(
        f'''select E_id,duration,exam_time from Exam where (Exam.C_id = '{IC_info[2]}'); ''')
    print("ic_dash")
    print(papers)
    return render_template("IC_dashboard.html", IC_info=IC_info, papers=papers)


@app.route('/edit_paper/<E_id>')
def edit_paper(E_id):
    print(E_id)
    return "Here you edit the paper "
