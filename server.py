from flask import Flask, url_for, request, redirect,jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import sys
from time import time



app = Flask(__name__)
CORS(app, support_credentials=True)



app.debug = True



@app.route('/')
def index():return 'Hello, found anything? this is a 501'

#Routing FN Def

#//////////////////// ELITE 3 \\\\\\\\\\\\\\\\\\\\\

@app.route('/elite_add',methods=['POST'])
def elite_add():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="elite":pass
    else: return "Permission Denied"

    uname=request.form.get('u_name')
    email=request.form.get('u_email')
    mobile=request.form.get('u_mob')
    course=request.form.get('u_course')
    tc=request.form.get('u_tc')
    bknifty=request.form.get('u_bknifty')
    ack_status=elite_add_user(uname,email,mobile,course,tc,bknifty)
    return ack_status


@app.route('/elite_fetach_alluser',methods=['POST'])
def elite_fetach_alluser():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="elite":pass
    else: return "Permission Denied"

    ack_status=elite_fetach_alluser()
    return ack_status








#//////////////////// ADMIN 6 \\\\\\\\\\\\\\\\\\\\\

# ========= Basic POST Section ===========

@app.route('/basic_link',methods=['POST'])
def basic_post_link():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="admin_b" or user_type=="elite":pass
    else: return "Permission Denied"

    name=request.form.get('name')
    linkno=request.form.get('linkno')
    link=request.form.get('link')
    ack_status=update_link("Basic_links",linkno,name,link)
    return ack_status

@app.route('/basic_msg',methods=['POST'])
def basic_post_msg():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="admin_b" or user_type=="elite":pass
    else: return "Permission Denied"

    msg=request.form.get('msg')
    ack_status=add_msg("Basic_msg",msg)
    return ack_status

@app.route('/del_basic_msg',methods=['POST'])
def del_basic_post_msg():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="admin_b" or user_type=="elite":pass
    else: return "Permission Denied"
    
    ts=request.form.get('ts')
    return_data=del_msg("Basic_msg",ts)
    return return_data


# ========= Pro POST Section ===========

@app.route('/pro_link',methods=['POST'])
def pro_post_link():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="admin_p" or user_type=="elite":pass
    else: return "Permission Denied"

    name=request.form.get('name')
    linkno=request.form.get('linkno')
    link=request.form.get('link')
    ack_status=update_link("Pro_links",linkno,name,link)
    return ack_status


@app.route('/pro_msg',methods=['POST'])
def pro_post_msg():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="admin_p" or user_type=="elite":pass
    else: return "Permission Denied"
    
    msg=request.form.get('msg')
    msg_type=request.form.get('type')
    ack_status=add_msg("Pro_msg",msg,msg_type)
    return ack_status

@app.route('/del_pro_msg',methods=['POST'])
def del_pro_post_msg():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="admin_p" or user_type=="elite":pass
    else: return "Permission Denied"
    
    ts=request.form.get('ts')
    return_data=del_msg("Pro_msg",ts)
    return return_data



#//////////////////// CLIENT 5 \\\\\\\\\\\\\\\\\\\\\


# ============= Verify client ===============
@app.route('/verify_user',methods=['POST'])
def client_verify():
    email=request.form.get('email')
    #print(email, file=sys.stdout)
    return_data=verify_client_db(email)
    return return_data

# ========Verify admin after verification ===============
@app.route('/verify_admin',methods=['POST'])
def admin_verify():
    
    email=request.form.get('email')
    user_type=detect_user_type(email)
    if user_type=="admin_p":return "pro"
    elif user_type=="admin_b":return "foundation"
    elif user_type=="elite":return "elite"
    else: return "err"


# ========= Common Get-Link client ===========
@app.route('/get_links',methods=['POST'])
def common_get_link_client():

    email=request.form.get('email')
    user_type=detect_user_type(email)
    #user_type=detect_user_type('adityasuryan1993@gmail.com')
    if user_type=="zero":tablename="none"
    elif user_type=="foundation" or user_type=="admin_b" or user_type=="elite":tablename="Basic_links"
    elif user_type=="pro full" or user_type=="admin_p" or user_type=="elite":tablename="Pro_links"
    elif user_type=="pro partial" or user_type=="admin_p" or user_type=="elite":tablename="Pro_links"
    else:tablename="none"
    
    return_data=fetch_link(tablename)
    return jsonify(return_data)

# ========= Common Get-msg client ===========
@app.route('/get_msg',methods=['POST'])
def common_get_msg_client():
    param="1"

    email=request.form.get('email')
    user_type=detect_user_type(email)
    #user_type=detect_user_type('adityasuryan1993@gmail.com')
    if user_type=="zero":tablename="none"
    elif user_type=="foundation" or user_type=="admin_b" or user_type=="elite":tablename="Basic_msg"
    elif user_type=="pro full":
        tablename="Pro_msg"
        param=user_type
    elif user_type=="pro partial":
        tablename="Pro_msg"
        param=user_type
    else:tablename="unk"

    print("sending tablename:"+tablename+" utype="+user_type)
    return_data=fetch_msg(tablename,param)
    return jsonify(return_data)

# ====== Splecial Route for pro admin get msg =============
@app.route('/get_msg_pro_admin',methods=['POST'])
def get_msg_pro_admin():
    #verification for every request
    email=request.form.get('email')
    user_type=detect_user_type(email)
    #user_type=detect_user_type('adityasuryan1993@gmail.com')
    if user_type=="admin_p" or user_type=="elite":pass
    else:return "Permission Denied"
    return_data=fetch_msg_pro_admin()
    return jsonify(return_data)





#/////////////////////////SQL Func Def\\\\\\\\\\\\\\\\\\\\\\

def create_table(db_conn):
    print("[+] Creating New Table")
    c = db_conn.cursor()
    #For Basic_links
    try:
        c.execute('''CREATE TABLE Basic_links (
            timestamp varchar(255) NOT NULL,
            n1 varchar(255),
            n2 varchar(255),
            n3 varchar(255),
            n4 varchar(255),
            n5 varchar(255),
            n6 varchar(255),
            link1 varchar(255),
            link2 varchar(255),
            link3 varchar(255),
            link4 varchar(255),
            link5 varchar(255),
            link6 varchar(255),
            new_push_flag varchar(255)
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )

    #For Pro_links
    try:
        c.execute('''CREATE TABLE Pro_links (
            timestamp varchar(255) NOT NULL,
            n1 varchar(255),
            n2 varchar(255),
            n3 varchar(255),
            n4 varchar(255),
            n5 varchar(255),
            n6 varchar(255),
            link1 varchar(255),
            link2 varchar(255),
            link3 varchar(255),
            link4 varchar(255),
            link5 varchar(255),
            link6 varchar(255),
            new_push_flag varchar(255)
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )

    #For Basic_msg
    try:
        c.execute('''CREATE TABLE Basic_msg (
            timestamp varchar(255) NOT NULL,
            msg varchar(255)
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )

    #For Pro_msg
    try:
        c.execute('''CREATE TABLE Pro_msg (
            timestamp varchar(255) NOT NULL,
            msg_type varchar(255),
            msg varchar(255)
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )

    #For Client_base
    try:
        c.execute('''CREATE TABLE Client_base (
            name varchar(255),
            email varchar(255),
            phone varchar(255),
            course varchar(255),
            tredcode varchar(255),
            index_access varchar(255)
            )''')
        db_conn.commit()
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )


def verify_client_db(email):
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()

    query=r"SELECT email from Client_base WHERE email='{}' ;".format(email)
    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        reply=c.fetchall()
        print(reply)
        if len(reply)>=1:return "success"
        else: return "err"
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return "err"


def detect_user_type(email):
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()

    query=r"SELECT course from Client_base WHERE email='{}' ;".format(email)
    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        reply=c.fetchall()
        #print(reply)
        reply=str(reply[0][0])
        reply=reply.lower()
        return reply
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return None


#admin
def update_link(tablename,linkno,name="",link=""):
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()
    nameno="n"+str(linkno)
    linkno="link"+str(linkno)

    curr_ts=time()

    query=r"UPDATE {} SET timestamp='{}', {}='{}',{}='{}' ;".format(tablename,curr_ts,linkno,link,nameno,name)
    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        return "link_upd_success"
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return "error_adding_link"



def fetch_link(tablename):
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()

    query=r"SELECT * from {} ;".format(tablename)
    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        reply=c.fetchall()
        print(reply)
        return reply
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return None

#admin
def add_msg(tablename,msg,msg_type=None):
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()
    curr_ts=time()

    if msg_type:query=r"INSERT INTO Pro_msg (timestamp,msg_type,msg)VALUES( '{}','{}','{}' ) ;".format(curr_ts,msg_type,msg)
    else:query=r"INSERT INTO {} (timestamp,msg)VALUES( '{}','{}' ) ;".format(tablename,curr_ts,msg)

    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        return "msg_upd_success"
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return "error_msg_upd"

#common fn for pro, baisc fetch
def fetch_msg(tablename,msg_type="1"):
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()
    
    #get latest 10 msg
    if msg_type=="pro partial":msg_type="msg_type='pro partial' or msg_type='all'  "
    elif msg_type=="pro full":msg_type="msg_type='pro full' or msg_type='all' "
    elif msg_type=="foundation":msg_type="1"

    query=r"SELECT * FROM {} Where {} ORDER BY rowid DESC limit 10 ;".format(tablename,msg_type)
    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        reply=c.fetchall()
        print(reply)
        return reply
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return None

def fetch_msg_pro_admin():
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()
    
    query=r"SELECT * FROM Pro_msg ORDER BY rowid DESC limit 10 ;"
    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        reply=c.fetchall()
        print(reply)
        return reply
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return None


def del_msg(tablename,ts,sub_course=None):
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()

    if sub_course!=None:
        query=r"Delete from {} Where timestamp='{}' and msg_type='{}' ;".format(tablename,ts,sub_course)
    else:query=r"Delete from {} Where timestamp='{}' ;".format(tablename,ts)

    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        return "success"
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return "err"



# Elite fn Def
def elite_add_user(uname,email,mobile,course,tc,bknifty):
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()
    
    query=r"INSERT INTO Client_base (name,email,phone,course,tredcode,index_access)VALUES('{}','{}','{}','{}','{}','{}') ;".format(uname,email,mobile,course,tc,bknifty)
    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        return "success"
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return "err"


def elite_fetach_alluser():
    db_conn = sqlite3.connect('tcm.db')
    c = db_conn.cursor()
    
    query=r"SELECT * FROM Client_base ;"
    print(query)
    try:
        c.execute(query)
        db_conn.commit()
        reply=c.fetchall()
        return reply
    except sqlite3.OperationalError as e:
        print("[-] "+str(e) )
        return "err"








#==================== Main calling =================

if __name__ == '__main__':
	#db init config
    db_conn = sqlite3.connect('tcm.db')
    create_table(db_conn)
    c = db_conn.cursor()
    default0=r"INSERT INTO Basic_links (timestamp,link1,link2 ,link3,link4)VALUES('0', '0','0','0','0');"
    default1=r"INSERT INTO Pro_links (timestamp,link1,link2 ,link3,link4)VALUES('0', '0','0','0','0');"
    del0=r"DELETE from Basic_links where rowid!=1"
    del1=r"DELETE from Pro_links where rowid!=1"
    c.execute(default0)
    c.execute(default1)
    c.execute(del0)
    c.execute(del1)
    db_conn.commit()
    db_conn.close()


    app.run(host='0.0.0.0', port=5000, debug=True)
