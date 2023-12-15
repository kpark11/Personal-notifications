# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 01:12:40 2023

@author: brian
"""
import email, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename

import requests
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt



path = "https://weather.com/weather/tenday/l/Knoxville+TN?canonicalCityId=626ef612d09792fa3f39bfb5ad2b6808faf39bd6c597c5d8c7301e27cec2ed4a"


def getWeather(path):
    x = requests.get(path)
    soup = BeautifulSoup(x.content, 'html.parser')
                
    content = []
    cont_day = []
    cont_temp = []
    cont_rain = []
    for i in range(20):        
        content_day = soup.find_all("div",{"data-testid":"DailyContent"})[i]
        line1 = '------------------------------------------------------' + '\n'
        
        time = content_day.find('h3').text
        line2 = f'{time}\n'
        cont_day.append(time)
        
        
        temp = content_day.find('span',{'data-testid':'TemperatureValue'}).text
        line3 = '------' + '\n'
        line5 = f'Temperature: {temp}'.format(temp=temp) + '\n'
        temp_num = temp[:-1]
        temp_num = int(temp_num)
        cont_temp.append(temp_num)
        
        precipitation = content_day.find('span',{'class':'DailyContent--value--1Jers'}).text
        line6 = '------' + '\n'
        line7 = 'Precipitation percentage (if not, Wind): {precipitation}'.format(precipitation=precipitation) + '\n'
        prec_num = precipitation[:-1]
        prec_num = int(prec_num)
        cont_rain.append(prec_num)
        
        summary = content_day.find('p',{'data-testid':'wxPhrase'}).text
        line9 = '------' + '\n'
        line10 = 'Summary: {summary}'.format(summary=summary) + '\n'

        line12 = '\n'
        holy = line1+line2+line3+line5+line6+line7+line9+line10+line12
        print(holy)
        content.append(holy)
    
    report = ''.join(content).strip()
    
    
    
    ###############################################
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(cont_day,cont_temp,marker='o',markersize=15,mfc ='r')
    fig.autofmt_xdate(rotation=45)
    ax.set_ylabel(r'Temperature ($^o$F)',fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    
    plt.savefig('temp.png', format='png')

    ###############################################
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(cont_day,cont_rain,marker='o',markersize=15,mfc ='r')
    fig.autofmt_xdate(rotation=45)
    ax.set_ylabel('Rain (%)',fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    
    plt.savefig('rain.png', format='png')
    
    ###############################################
        
    
    return report

def get_credential():
    with open("credential.txt", 'r') as file:
        parts = file.read()
    credential = parts.split(",")
    return credential
        


def send_email_via_email(
    receiver: str,
    message: str,
    sender_credentials: list,
    subject: str,

):

    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    
    sender_email = sender_credentials[0]
    email_password = sender_credentials[1]
    ################################################################
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver
    msg.attach(MIMEText(message))
    ################################################################
        

    # Now add the related image to the html part.
    with open("temp.png", 'rb') as img:
        part = MIMEApplication(img.read(),Name=basename("temp.png"))
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename("temp.png")
    msg.attach(part)
    
    with open("rain.png", 'rb') as img:
        part = MIMEApplication(img.read(),Name=basename("rain.png"))
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename("rain.png")
    msg.attach(part)
    
    
    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        #email.sendmail(sender_email, receiver_email, email_message.encode('utf-8'))
        email.sendmail(sender_email,receiver,msg.as_string())



def main():
    
    message = getWeather(path)

    receiver = "kimanpark33@gmail.com"
    receiver1 = "carpenter.abby25@gmail.com"

    sender_credentials = get_credential()    
    try:
        #Email
        send_email_via_email(receiver, message, sender_credentials,'Weather Report')
        #send_email_via_email(receiver1, message, sender_credentials,'Weather Report')
        print('\n')
        print('Email Sent!')

    except:
        print('\n')
        print('error')        
    
    
if __name__ == "__main__":
    main()






