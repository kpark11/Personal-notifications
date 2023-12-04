# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:21:45 2023

@author: brian
"""

import email, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup




path = "http://www.fortunecookiemessage.com/"

def getFortune(path):
    x = requests.get(path)
    soup = BeautifulSoup(x.content, 'html.parser')
    fortune = soup.find("div",{"class":"quote"}).text
    print(fortune)
        
    
    return fortune


def send_email_via_email(
    receiver: str,
    message: str,
    sender_credentials: tuple,
    subject: str,
):

    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    
    sender_email, email_password = sender_credentials
    
    ################################################################
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver
    msg.attach(MIMEText(message))
    ################################################################
        
    
    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        #email.sendmail(sender_email, receiver_email, email_message.encode('utf-8'))
        email.sendmail(sender_email,receiver,msg.as_string())





def main():
    
    message = getFortune(path)
    message1 = getFortune(path)


    receiver = "kimanpark33@gmail.com"
    receiver1 = "carpenter.abby25@gmail.com"

    sender_credentials = ("kimanpark33@gmail.com", "byab pntv aygn eqbo")
    
    try:
        #Email
        send_email_via_email(receiver, message, sender_credentials,'Fortune for the day')
        send_email_via_email(receiver1, message1, sender_credentials,'Fortune for the day')
        print('\n')
        print('Email Sent!')

    except:
        print('\n')
        print('error')        
    
    
if __name__ == "__main__":
    main()
