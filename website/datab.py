import mysql.connector as c

def connect():
    try:
        mydb = c.connect(
                host="localhost",
                port="3306",
                user="root",
                passwd="vatsal",
                database="dbs_vi"
            )
        return mydb
    except:
        print("Connection couldn't be established")
        exit()
        return None

def s_login(mydb, ID, passw):
    cur=mydb.cursor()
    
    
    # cur=mydb.cursor()
    # cur.execute('''SHOW tables''')
    # result = cur.fetchall()
    # for db in result:
    #     print(db)
