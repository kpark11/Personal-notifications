# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:21:45 2023

@author: brian
"""

import requests
from bs4 import BeautifulSoup

import email, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from os.path import basename
import os
import numpy as np
import random

# Define the URL for the quotes page
url = "https://www.inspiringquotes.com/"

def  getMotivation():
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    #if response.status_code == 200:
    try:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the sections containing quotes
        quote = soup.find('h1').text.strip()
        author = soup.find('div', {'class':'IQDailyInspiration__author'}).text.strip()
        
        print("Quote: " + quote + '\n\n' + 'Author: ' + author)
        
        return "Quote: " + quote + '\n\n' + 'Author: ' + author
    except ValueError:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return ""

    


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
    
    valid = ["jpg", "jpeg", "png"]
    pics = [x for x in os.listdir() if x.split('.')[-1].lower() in valid]
    pic = random.choices(pics)[0]
    
    print(pic)
    with open(pic, 'rb') as img:
        part = MIMEApplication(img.read(),Name=basename(pic))
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(pic)
    msg.attach(part)
    ################################################################
        
    
    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        #email.sendmail(sender_email, receiver_email, email_message.encode('utf-8'))
        email.sendmail(sender_email,receiver,msg.as_string())





def main():
    
    message = getMotivation()

    receiver = "kimanpark33@gmail.com"

    sender_credentials = ("kimanpark33@gmail.com", "byab pntv aygn eqbo")
    
    try:
        #Email
        send_email_via_email(receiver, message, sender_credentials,'Motivation')
        print('\n')
        print('Email Sent!')

    except:
        print('\n')
        print('error')        
    
    
if __name__ == "__main__":
    main()
