# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:55:01 2021

@author: HP
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class MailClient:
    
    def __init__(self):
        self.from_email='dragonslayer2158@gmail.com'
        self.api_key='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'
    def send(self,to,sub,content):
        message = Mail(from_email=self.from_email,to_emails=to, subject=sub,html_content= content)
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)