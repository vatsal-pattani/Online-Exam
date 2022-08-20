import psycopg2 as c
import os


def connect():
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if DATABASE_URL:
            mydb = c.connect(DATABASE_URL, sslmode='require')
        else:
            mydb = c.connect(
                host="localhost",
                port="5432",
                user="postgres",
                password=os.environ.get("DBS_VI_PASSWORD"),
                database="dbs_vi"
            )

        return mydb

    except Exception as exec:
        print("Connection couldn't be established")
        # print(exec)
        exit()


def s_login(mydb, ID, passw):
    cur = mydb.cursor()

    # cur=mydb.cursor()
    # cur.execute('''SHOW tables''')
    # result = cur.fetchall()
    # for db in result:
    #     # print(db)
