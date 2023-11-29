# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 01:12:40 2023

@author: brian
"""
import email, smtplib, ssl

# used for MMS
from email import encoders
from email.parser import Parser
from email.policy import default


import requests
from bs4 import BeautifulSoup
import json

path = "https://weather.com/weather/tenday/l/Knoxville+TN?canonicalCityId=626ef612d09792fa3f39bfb5ad2b6808faf39bd6c597c5d8c7301e27cec2ed4a"


def getWeather(path):
    x = requests.get(path)
    soup = BeautifulSoup(x.content, 'html5lib')
                
    content = []
    for i in range(20):        
        content_day = soup.find_all("div",{"data-testid":"DailyContent"})[i]
        line1 = '------------------------------------------------------' + '\n'
        
        time = content_day.find('h3').text
        line2 = f'{time}\n'
        
        
        temp = content_day.find('span',{'data-testid':'TemperatureValue'}).text
        line3 = '------' + '\n'
        line5 = f'Temperature: {temp}'.format(temp=temp) + '\n'
        
        precipitation = content_day.find('span',{'class':'DailyContent--value--1Jers'}).text
        line6 = '------' + '\n'
        line7 = 'Precipitation percentage (if not, Wind): {precipitation}'.format(precipitation=precipitation) + '\n'
        
        summary = content_day.find('p',{'data-testid':'wxPhrase'}).text
        line9 = '------' + '\n'
        line10 = 'Summary: {summary}'.format(summary=summary) + '\n'

        line12 = '\n'
        holy = line1+line2+line3+line5+line6+line7+line9+line10+line12
        print(holy)
        content.append(holy)
    
    report = ''.join(content).strip()
    return report

def send_email_via_email(
    receiver: str,
    message: str,
    sender_credentials: tuple,
    subject: str = "sent using etext",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = receiver
        
    'From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}'
    email_message = f"From: {sender_email}\r\nTo: {receiver}\r\nSubject: {subject}\r\n\r\n{message}".format(sender_email=sender_email,receiver=receiver,subject=subject,message=message)
    
    
    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message.encode('utf-8'))


def main():
    
    text = getWeather(path)

    receiver = "kimanpark33@gmail.com"
    receiver1 = "carpenter.abby25@gmail.com"
    message = text

    sender_credentials = ("kimanpark33@gmail.com", "byab pntv aygn eqbo")
    
    try:
        #Email
        send_email_via_email(receiver, message, sender_credentials,subject='Weather Report')
        send_email_via_email(receiver1, message, sender_credentials,subject='Weather Report')
        print('Email Sent!')

    except:
        print('error')        
    
    
if __name__ == "__main__":
    main()






