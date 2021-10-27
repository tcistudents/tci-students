import pandas as pds
import sqlite3 

global db_filename
db_filename='tcm.db'

#fn def

def clear_prev_data():
    db_conn = sqlite3.connect(db_filename)
    c = db_conn.cursor()

    query=r"DELETE FROM Client_base ;"
    
    #print(query)
    try:
        c.execute(query)
        db_conn.commit()
        return "del_success"
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return "error_del"


def add_msg(name,email,ph,course,tc,index):
    db_conn = sqlite3.connect(db_filename)
    c = db_conn.cursor()

    query=r"INSERT INTO Client_base (name,email,phone,course,tredcode,index_access)VALUES( '{}','{}','{}','{}','{}','{}' ) ;".format(name,email,ph,course,tc,index)
    
    #print(query)
    try:
        c.execute(query)
        db_conn.commit()
        return "insert_row_success"
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return "error_row_ins"



#main exec

file =('stu data.xlsx')
df = pds.read_excel(file,engine='openpyxl',dtype=str)

#drop empty rows
df=df.dropna()

clear_prev_data()
for index, row in df.iterrows():
    add_msg(row[0],row[1],row[2],row[3],row[4],row[5])

print("[+] Excel to Database Upload Completed")
