# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 19:22:55 2021

@author: HP
"""


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from UserModel import UserModel
app = Flask(__name__)
app.secret_key = 'a'

  
app.config['MYSQL_HOST'] = "localhost"#"remote.mysql"
app.config['MYSQL_USER'] = "root"#"username for remote"
app.config['MYSQL_PASSWORD'] = ""#"password of the remote for remote"
app.config['MYSQL_DB'] = "test1"
mysql = MySQL(app)
user_model = UserModel(mysql)
@app.route('/')#app.route(rule,options)
def homer():
    
    return render_template('home.html')
    
@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ' '
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        response = user_model.validate_user(username,password)
        print (response)
        if response != None:
            session['loggedin'] = True
            session['username'] = response['name']
            user_type=response['type']
            msg = 'Logged in successfully !'
            msg = 'Logged in successfully !'
            if user_type == 'admin':
                count=user_model.get_unsolved_complaints()
                values = user_model.admin_dash_purchase_details()
                trend = user_model.admin_dash_purchase_trend()
                return render_template('addashboard.html',count=count[0],values=values,trend=trend)
            else:
                details=user_model.get_user_details(username)
                session['name'] = details[5]
                values = user_model.dash_purchase_details(username)
                trend = user_model.dash_purchase_trend(username)
                count=user_model.get_new_notifications_count(username)
                return render_template('dashboard.html', data = username , name = session['name'],values=values,trend=trend,count=count)
        else:
            msg = 'Incorrect username / password !'
    return render_template('home.html', msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        response = user_model.register(name,username,email,password)
        if response :
            msg = 'You have successfully registered !'
            return render_template('home.html', msg = msg)
            #TEXT = "Hello "+username + ",\n\n"+ """Thanks for applying registring at smartinterns """ 
            #message  = 'Subject: {}\n\n{}'.format("smartinterns Carrers", TEXT)
            #sendmail(TEXT,email)
            #sendgridmail(email,TEXT)'''
        else :
            msg = 'Account already exists !'
        
    return render_template('register.html', msg = msg)



@app.route('/dashboard')
def dashboard():
        username = session['username'] 
        values = user_model.dash_purchase_details(username)
        trend = user_model.dash_purchase_trend(username)
        count=user_model.get_new_notifications_count(username)
        return render_template('/dashboard.html',data = username , name=session['name'],values=values,trend=trend,count=count)
   #if 'loggedin' in session == True:
        #return render_template('/dashboard.html')
   # else:
   
        #return render_template('/home.html',msg='Please login with your credentials')
        
@app.route('/addashboard')
def addashboard():
         count=user_model.get_unsolved_complaints()
         values = user_model.admin_dash_purchase_details()
         trend = user_model.admin_dash_purchase_trend()
         return render_template('addashboard.html',count=count[0],values=values,trend=trend)

@app.route('/user')
def user():
    
    username = session['username'] 
    details=user_model.get_user_details(username)
    count=user_model.get_new_notifications_count(username)
    return render_template('/user.html',data = username , name=session['name'],details=details,count=count)

@app.route('/user_edit',methods =['GET', 'POST'])
def useredit():
    
    print(request.form)
    if request.method == 'POST' :
        username = session['username']
        name = request.form['first_name']
        address = request.form['address']
        phone = request.form['pnumber']
        email = request.form['email']
        if user_model.update_user_details(username,name,address,phone,email):
            details=user_model.get_user_details(username)
            count=user_model.get_new_notifications_count(username)
            return render_template('/user.html',data = username , name=session['name'],details=details,count=count)
            
     
    else:
        username = session['username'] 
        details=user_model.get_user_details(username)
        count=user_model.get_new_notifications_count(username)
        return render_template('/user_edit.html',data = username , name=session['name'],details=details,count=count)

@app.route('/tables')
def table():
    return render_template('/tables.html')


@app.route('/purchasehistory')
def history():
    username = session['username'] 
    details,colnames=user_model.get_user_purchases(username)
    count=user_model.get_new_notifications_count(username)
    return render_template('/purchasehistory.html',data = username , name=session['name'],details=details,colnames=colnames,count=count)


@app.route('/payments')
def payments():
    username = session['username'] 
    details,colnames=user_model.get_pending_payments(username)
    count=user_model.get_new_notifications_count(username)
    if details == None:
        details = []
    return render_template('/pendingpayments.html',data = username , name=session['name'],details=details,colnames=colnames,count=count)
 
@app.route('/dopayment',methods =['GET', 'POST'])
def dopayments():
    if request.method == 'GET' :
        pid = request.args.get("pid").strip()
        username = session['username']
        details=user_model.get_user_payment_details(username,pid)
        count=user_model.get_new_notifications_count(username)
        return render_template('/dopayment.html', name=session['name'],details=details,count=count)
    elif request.method == 'POST' :
        pid=request.form['pid']
        amountpaying=request.form['amountpaying']
        username=session['username']
        user_model.do_payment(pid,amountpaying)
        details,colnames=user_model.get_pending_payments(username)
        count=user_model.get_new_notifications_count(username)
        if details == None:
            details = []
        return render_template('/pendingpayments.html',data = username , name=session['name'],details=details,colnames=colnames,count=count)
        
@app.route('/complaints', methods =['GET', 'POST'])
def docomplaints():
    username = session['username']
    if request.method == 'POST' :
        phno = request.form['phno']
        email = request.form['email']
        message = request.form['message']
        response = user_model.register_complaints(username,phno,email,message)
    details,colnames=user_model.get_user_complaints(username)
    count=user_model.get_new_notifications_count(username)
    if details == None:
        details = []
    return render_template('/complaints.html',name=session['name'],details=details,colnames=colnames,data = username,count=count)

@app.route('/notifications', methods =['GET', 'POST'])
def notificationss():
    username = session['username']
    user_model.update_user_notifications(username)
    details,colnames=user_model.get_user_notifications(username)
    count=user_model.get_new_notifications_count(username)
    if details == None:
        details = []
    return render_template('/notifications.html',name=session['name'],details=details,colnames=colnames,data = username,count=count)


@app.route('/adcomplaints', methods =['GET', 'POST'])
def solvecomplaints():
    details,colnames=user_model.solve_user_complaints() 
    username=session['username']
    count=user_model.get_unsolved_complaints()
    if details == None:
        details = []
    return render_template('/adcomplaints.html',name=session['name'],details=details,colnames=colnames,data = username,count=count[0])
   
        
@app.route('/closecomplaints', methods =['GET', 'POST'])
def closecomplaints():
     if request.method == 'GET' :
        cid = request.args.get("cid").strip()
        count=user_model.get_unsolved_complaints()
        user_model.solved_user_complaints(cid)
        details,colnames=user_model.solve_user_complaints() 
        username=session['username']
        if details == None:
            details = []
        return render_template('/adcomplaints.html',name=session['name'],details=details,colnames=colnames,data = username,count=count[0])

@app.route('/adpayments')
def allpendingpayments():
    username = session['username'] 
    count=user_model.get_unsolved_complaints()
    details,colnames=user_model.get_all_pending_payments()
    if details == None:
        details = []
    return render_template('/adpendingpayments.html',data = username ,count= count[0], name=session['name'],details=details,colnames=colnames)

@app.route('/doalert')
def doalert():
     if request.method == 'GET' :
        pid = request.args.get("pid").strip()
        user_model.add_pending_alert(pid)
        details,colnames=user_model.get_all_pending_payments() 
        count=user_model.get_unsolved_complaints()
        username=session['username']
        if details == None:
            details = []
        return render_template('/adpendingpayments.html',name=session['name'],count=count[0],details=details,colnames=colnames,data = username)
        
    
@app.route('/viewuser')
def viewuser():
    if request.method == 'GET' :
        username=request.args.get("uname").strip()
        details=user_model.get_user_details(username)
        count=user_model.get_unsolved_complaints()
        return render_template('/viewuser.html',data = username ,details=details,count=count[0])
        
@app.route('/customers')
def customers():
    
    username = session['username'] 
    details,colnames=user_model.get_customer_details()
    count=user_model.get_unsolved_complaints()
    return render_template('/customers.html',data = username , name=session['name'],details=details,count=count[0],colnames=colnames)

@app.route('/purchases',methods =['GET', 'POST'])
def purchases():
    count=user_model.get_unsolved_complaints()
    details=user_model.get_all_users()
    if request.method == 'POST' :
        username = request.form['username']
        date = request.form['date']
        particulars=request.form['particulars']
        tamount = request.form['tamount']
        payingamt = request.form['payingamt']
        bamount = request.form['bamount']
        if int(bamount) == 0:
            status = "complete"
        status="pending"
        user_model.admin_billing(username,date,tamount,payingamt,bamount,particulars,status)
    return render_template('/purchases.html',count=count[0],details=details)


if __name__ == '__main__':
    app.run(debug=True,port=5000)#run in the webbrowser