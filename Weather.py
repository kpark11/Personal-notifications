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
import numpy as np
import os

import requests
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt




def getWeather(path):
    x = requests.get(path)
    soup = BeautifulSoup(x.content, 'html.parser')
    
    content = []
    cont_day = []
    cont_temp = []
    cont_rain = []
    try:
        for i in range(20):        
            content_day = soup.find_all("div",{"data-testid":"DailyContent"})[i]
            line1 = '------------------------------------------------------' + '\n'
            # Date and time
            time = content_day.find('h2').text
            line2 = f'{time}\n'
            cont_day.append(time)
            
            # Temperature
            temp = content_day.find('span',{'data-testid':'TemperatureValue'}).text
            line3 = '------' + '\n'
            line5 = f'Temperature: {temp}'.format(temp=temp) + '\n'
            temp_num = temp[:-1]
            temp_num = int(temp_num)
            cont_temp.append(temp_num)
            
            # Precipitation
            try:
                precipitation = content_day.find('span',{'data-testid':'PercentageValue'}).text
            except:
                precipitation = '0%'
            line6 = '------' + '\n'
            line7 = 'Precipitation percentage: {precipitation}'.format(precipitation=precipitation) + '\n'
            prec_num = precipitation[:-1]
            #print(precipitation)
            try:
                prec_num = int(prec_num)
            except ValueError:
                prec_num = 0
            
            cont_rain.append(prec_num)
            
            # Wind
            wind = content_day.find('span',{'data-testid':'Wind'}).text
            line8 = '------' + '\n'
            line9 = f'Wind: {wind}'.format(temp=temp) + '\n'
            
            summary = content_day.find('p',{'data-testid':'wxPhrase'}).text
            line10 = '------' + '\n'
            line11 = 'Summary: {summary}'.format(summary=summary) + '\n'
    
            line12 = '\n'
            holy = line1+line2+line3+line5+line6+line7+line8+line9+line10+line11+line12
            print(holy)
            content.append(holy)
        
        report = ''.join(content).strip()
        
        
        
        ###############################################
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(cont_day,cont_temp,marker='o',markersize=15,mfc ='r')
        fig.autofmt_xdate(rotation=45)
        ax.set_ylabel(r'Temperature ($^o$F)',fontsize=20)
        
        major_ticks = np.arange(0, 111, 10)
        minor_ticks = np.arange(0, 111, 5)
        
        ax.set_yticks(major_ticks)
        ax.set_yticks(minor_ticks, minor=True)
        ax.set_ylim(0,110)
        ax.grid(True)
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=15)
        
        plt.savefig('temp.png', format='png')
    
        ###############################################
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(cont_day,cont_rain,marker='o',markersize=15,mfc ='r')
        fig.autofmt_xdate(rotation=45)
        ax.set_ylabel('Rain (%)',fontsize=20)
        ax.set_ylim(-10,110)
        ax.grid(True)
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=15)
        
        plt.savefig('rain.png', format='png')
        
        ###############################################
        return report
    except:
        return 'Error'

def get_credential():
    with open("credential.txt", 'r') as file:
        parts = file.read()
    credential = parts.split(",")
    return credential
        
def cleanDir():
    if os.path.exists("temp.png"):
        os.remove('temp.png')
    else:
        print("The temp.png does not exist")
        
    if os.path.exists("rain.png"):
        os.remove('rain.png')
    else:
        print("The rain.png does not exist")

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
        
    try:
    # Now add the related image to the html part.
        with open("temp.png", 'rb') as img:
            part = MIMEApplication(img.read(),Name=basename("temp.png"))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename("temp.png")
        msg.attach(part)
        
        with open("rain.png", 'rb') as img:
            part = MIMEApplication(img.read(),Name=basename("rain.png"))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename("rain.png")
        msg.attach(part)
    except:
        pass
    
        
    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        #email.sendmail(sender_email, receiver_email, email_message.encode('utf-8'))
        email.sendmail(sender_email,receiver,msg.as_string())



Knox_path = "https://weather.com/weather/tenday/l/Knoxville+TN?canonicalCityId=626ef612d09792fa3f39bfb5ad2b6808faf39bd6c597c5d8c7301e27cec2ed4a"
Hosch_path = "https://weather.com/weather/tenday/l/5045bdcbf6598772976f065c7b985bc9cd9debf133488de3e480c4ea77345d59"

def main():
    
    receiver = "kimanpark33@gmail.com"
    sender_credentials = get_credential()
    
    message = getWeather(Knox_path)
    
    if message != 'Error':
        #Email
        send_email_via_email(receiver, message, sender_credentials,'Knoxville TN Weather Report')
        print('\n')
        print('Knoxville Email Sent!')
    else:
        send_email_via_email(receiver, message, sender_credentials,'Knoxville TN Weather Report (Error)')
        print('\n')
        print('Error!')
        
    cleanDir()
        
    message = getWeather(Hosch_path)
    
    if message != 'Error':
        #Email
        send_email_via_email(receiver, message, sender_credentials,'Hoschton GA Weather Report')
        print('Hoschton Email Sent!')
        print('\n')
    else:
        send_email_via_email(receiver, message, sender_credentials,'Hoschton GA Weather Report (Error)')
        print('\n')
        print('Error!')
        
    cleanDir()
        
    
if __name__ == "__main__":
    main()
    





