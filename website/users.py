from psycopg2 import ProgrammingError
from .datab import connect

# class User:
S_query = '''select S_id,S_Name 
             from Student as temp_s 
             where (S_id = '{ID}') and (S_Password = '{passw}'); -- authentication of the user, Fetched name of the student
             -- After Student logs in, his S_id, S_Name will be stored'''

IC_query = '''  select IC_Name,title,C_id 
                from Course 
                where (IC_id = '{ID}') and (IC_Password = '{passw}');'''

Ad_query = '''  select Ad_name 
                from Admin_info 
                where (Ad_id = '{ID}') and (Ad_Password = '{passw}');'''


def verify_in_db(ID, passw, log_type):
    db = connect()
    cur = db.cursor()
    query = ""
    # print(log_type)
    if log_type == "Student":
        query = S_query
    elif log_type == "IC":
        query = IC_query
    elif log_type == "Admin":
        query = Ad_query

    # # print("This is query:**************************************")
    # # print(query.format(ID=ID, passw=passw))

    cur.execute(query.format(ID=ID, passw=passw))

    result = cur.fetchall()
    cur.close()
    if not result:
        return False

    else:
        # print(result)
        # print(type(result[0]))
        return True


def getCourses(ID):
    db = connect()

    cur = db.cursor()
    cur.execute(f'''
                    select title,IC_Name 
                    from takes natural join Course
                    where S_id = '{ID}';
                    ''')
    courses = cur.fetchall()
    cur.close()
    return courses


def execute(str):
    db = connect()
    db.autocommit = True
    cur = db.cursor()
    cur.execute(str)
    q_result = []
    try:
        q_result = cur.fetchall()  # List of tuples. Each tuple is a row
    except ProgrammingError as progError:
        pass

    cur.close()
    return q_result
# class Student():

#     def __init__(self,ID,passw):
#         self.ID=ID
#         self.passw=passw

#     def getCourses(self):
#         db=connect()

#         cur=db.cursor()
#         cur.execute(f'''
#                     select title,IC_Name
#                     from takes natural join Course
#                     where S_id = '{self.ID}';
#                     ''')
#         courses=cur.fetchall()
#         cur.close()
#         return courses
