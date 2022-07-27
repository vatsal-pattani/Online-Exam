import mysql.connector as c
import os



def connect():
    try:
        mydb = c.connect(
            host="localhost",
            port="3306",
            user="root",
            passwd=os.environ.get("DBS_VI_PASSWORD"),
            database="dbs_vi"
        )
        return mydb
    except Exception as exec:
        print("Connection couldn't be established")
        print(exec)
        exit()



def s_login(mydb, ID, passw):
    cur = mydb.cursor()

    # cur=mydb.cursor()
    # cur.execute('''SHOW tables''')
    # result = cur.fetchall()
    # for db in result:
    #     print(db)
