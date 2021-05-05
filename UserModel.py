# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 18:53:30 2021

@author: HP
"""


class UserModel:
    
    def __init__(self,dbobj):
        
        self.dbobj = dbobj
    
    def validate_user(self,username,password):
        
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password ))
        account = cursor.fetchone()
        print (account)
        if account :
            response = {}

            response['name']=account[0]
            response['type']=account[3]
            
            return response
        else:
            return None
    def register(self,name,username,email,password):
        
        if self.get_user_details(username) != None:
            return False
        else:
            cursor = self.dbobj.connection.cursor()
            cursor.execute('INSERT INTO login VALUES ( % s, % s, % s,%s)', (username,password,email,'user'))
            cursor.execute('INSERT INTO userdetails(username,name) VALUES ( % s,% s)', (username,name))
            cursor.execute('INSERT INTO notification VALUES ( NULL,NOW(), % s, % s,% s,% s)',(username,"Profile Completion","Please Complete Your Profile Details","new"))
            self.dbobj.connection.commit()
            self.dbobj.connection.commit()
            return True
            
            
    
    def get_user_details(self,username):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT * FROM login,userdetails WHERE login.username = userdetails.username and login.username =  % s', (username, ))
        account = cursor.fetchone()
        if account:
            return account
        else:
            return None
                
    def update_user_details(self,username,name,address,phone,email):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('UPDATE `userdetails` SET name =%s,address=%s,phone=%s WHERE username = %s' ,(name,address,phone,username) )
        self.dbobj.connection.commit()
        cursor.execute('UPDATE login SET email=%s WHERE username = %s' ,(email,username) )
        self.dbobj.connection.commit()
        return True
    
    def get_user_purchases(self,username):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT `purchase_date`,`description`, `total_amount`, `paid_amount`,`balance_amount`,  `status` FROM purchase WHERE username =  % s', (username, ))
        account = cursor.fetchall()
        if account:
            return account, ['Date','Particulars','Total Amount','Paid Amount','Balance Amount','Status']
        else:
            return None
        
    def get_pending_payments(self,username):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT purchase_id ,`purchase_date`,`description`, `total_amount`, `paid_amount`,`balance_amount`,  `status` FROM purchase WHERE username =  % s AND status != "complete"', (username, ))
        account = cursor.fetchall()
        if account:
            return account, ['Date','Particulars','Total Amount','Paid Amount','Balance Amount','Status','Action']
        else:
            return None,['Date','Particulars','Total Amount','Paid Amount','Balance Amount','Status','Action']
    def get_user_payment_details(self,username,pid):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT purchase_id ,`purchase_date`,`description`, `total_amount`, `paid_amount`,`balance_amount`,  `status` FROM purchase WHERE username =  % s AND status != "complete" AND purchase_id=%s' , (username,int(pid) ))
        account = cursor.fetchall()
        if account:
            return account
        else:
            return None
    
    def do_payment(self,pid,amt):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('UPDATE `purchase` SET `balance_amount`= balance_amount-%s,paid_amount=paid_amount+%s WHERE purchase_id=%s',(amt,amt,pid))
        self.dbobj.connection.commit()
        cursor.execute('UPDATE `purchase` SET  `status`= "complete" WHERE balance_amount=0')
        self.dbobj.connection.commit()
        return True
    
    def register_complaints(self,username,phn,email,message):
        
            cursor = self.dbobj.connection.cursor()
            cursor.execute('INSERT INTO complaints VALUES ( NULL,% s,% s, % s, % s,NOW(),"pending")', (username,phn,email,message))
            self.dbobj.connection.commit()
            return True   
        
    def get_user_complaints(self,username):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT `cid`,`date`, `message`, `status` FROM complaints WHERE username =  % s', (username, ))
        
        account = cursor.fetchall()
        if account:
            return account, ['Complaint ID','Date','Message','Status']
        else:
            return None
        
    def solve_user_complaints(self):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT * FROM complaints' )
        account = cursor.fetchall()
        if account:
            return account, ['Complaint ID','Username','Phone Number','Email','Message','Date','Status','Action']
        else:
            return None
        
    def solved_user_complaints(self,cid):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('UPDATE `complaints` SET `status` = "solved" WHERE cid = %s',(cid,) )
        self.dbobj.connection.commit()
        cursor.execute('SELECT * FROM complaints' )
        account = cursor.fetchall()
        if account:
            return account, ['Complaint ID','Username','Phone Number','Email','Message','Date','Status']
        else:
            return None
       
    def get_all_pending_payments(self):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT purchase_id ,username  ,`purchase_date`,`description`, `total_amount`, `paid_amount`,`balance_amount`,  `status` FROM purchase WHERE status != "complete"')
        account = cursor.fetchall()
        if account:
            return account, ['Username','Date','Particulars','Total Amount','Paid Amount','Balance Amount','Status','Action']
        else:
            return None,['Username','Date','Particulars','Total Amount','Paid Amount','Balance Amount','Status','Action'] 
        
        
    def add_pending_alert(self,pid):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT * from purchase WHERE purchase_id = %s',(pid,))
        details=cursor.fetchone()
        #`purchase_id`, `username`, `purchase_date`, `total_amount`, `balance_amount`, `paid_amount`, `description`, `sta
        to=details[1]
        about='payment'
        content="You have a pending payment of Rs "+str(details[4])+" regarding the purchase id "+str(details[0])+" purchased on "+str(details[2])
        status="new"
        cursor.execute('INSERT INTO notification VALUES ( NULL,NOW(), % s, % s,% s,% s)',(to,about,content,status))
        self.dbobj.connection.commit()
        return True
        
    def get_unsolved_complaints(self):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM complaints WHERE status!="solved"' )
        account = cursor.fetchone()
        return account
        
    def dash_purchase_details(self,username):
         cursor = self.dbobj.connection.cursor()
         cursor.execute('SELECT status,COUNT(*) FROM purchase WHERE username = % s GROUP BY status' ,(username,))
         account = cursor.fetchall()
         completed = 0
         pending = 0
         if len(account) == 1:
             if account[0][0] == "complete":
                 completed = account[0][1]
             else:
                 pending = account[0][1]
         elif len(account)==2:
             completed = account[0][1]
             pending = account[1][1]
             
         total= completed + pending
         cursor = self.dbobj.connection.cursor()
         cursor.execute('SELECT COUNT(*) FROM complaints WHERE username=% s',(username,) )
         account = cursor.fetchone()
         complaints = account[0]
         return [completed,pending,total,complaints]
     
    def dash_purchase_trend(self,username):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT MONTHNAME(purchase_date),COUNT(*) FROM purchase WHERE username = % s GROUP BY MONTH(purchase_date)' ,(username,))
        account = cursor.fetchall()
        return account
    
    def get_user_notifications(self,username):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT `ndate`, `about`, `content` FROM notification WHERE `to` =% s ORDER BY ndate DESC',(username,) )
        account = cursor.fetchall()
        if len(account) > 0:
            return account,['Date','About','Content']
        else:
            return None,['Date','About','Content']
        
    def get_new_notifications_count(self,username):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM notification WHERE `to` =% s AND status = "new"',(username,) )
        account = cursor.fetchone()
        return account[0]
    
    def update_user_notifications(self,username):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('UPDATE notification SET status = "old" WHERE status ="new" AND `to` = % s',(username,))
        self.dbobj.connection.commit()
        return True
    
    def admin_dash_purchase_details(self):
         cursor = self.dbobj.connection.cursor()
         cursor.execute('SELECT status,COUNT(*) FROM purchase GROUP BY status')
         account = cursor.fetchall()
         completed = 0
         pending = 0
         if len(account) == 1:
             if account[0][0] == "complete":
                 completed = account[0][1]
             else:
                 pending = account[0][1]
         else:
             completed = account[0][1]
             pending = account[1][1]
             
         total= completed + pending
         cursor = self.dbobj.connection.cursor()
         cursor.execute('SELECT COUNT(*) FROM complaints WHERE status = "solved"')
         account = cursor.fetchone()
         solvedcomplaints = account[0]
         cursor.execute('SELECT COUNT(*) FROM complaints WHERE status != "solved"')
         account = cursor.fetchone()
         pendingcomplaints = account[0]
         cursor.execute('SELECT COUNT(*) FROM login WHERE type = "user"')
         account = cursor.fetchone()
         ucount=account[0]
         return [completed,pending,total,solvedcomplaints,pendingcomplaints,ucount]
        
    def admin_dash_purchase_trend(self):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT MONTHNAME(purchase_date),COUNT(*) FROM purchase GROUP BY MONTH(purchase_date)')
        account = cursor.fetchall()
        return account
    
    def get_customer_details(self):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT name,email,address,phone FROM login,userdetails WHERE login.username = userdetails.username and login.type !=  "admin"')
        account = cursor.fetchall()
        if account:
            return account,['Username','Email','Address','Phone Number']
        else:
            return None
        
    def admin_billing(self,username,date,tamount,payingamt,bamount,particulars,status):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('INSERT INTO purchase VALUES( NULL, % s, % s ,% s ,% s ,% s, % s ,% s)',(username,date,tamount,bamount,payingamt,particulars,status))
        self.dbobj.connection.commit()
        return True
    
    def get_all_users(self):
        cursor = self.dbobj.connection.cursor()
        cursor.execute('SELECT username FROM login WHERE type ="user"')
        account = cursor.fetchall()
        if len(account) > 0:
             return account
        else:
            return None
    
        
        
         
         
        