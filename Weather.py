# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 01:12:40 2023

@author: brian
"""
import email, smtplib, ssl
from providers import PROVIDERS

# used for MMS
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from providers import PROVIDERS

from os.path import basename

def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = "sent using etext",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

def send_mms_via_email(
    number: str,
    message: str,
    file_path: str,
    mime_maintype: str,
    mime_subtype: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = "sent using etext",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):

    sender_email, email_password = sender_credentials
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message=MIMEMultipart()
    email_message["Subject"] = subject
    email_message["From"] = sender_email
    email_message["To"] = receiver_email

    email_message.attach(MIMEText(message, "plain"))

    with open(file_path, "rb") as attachment:
        part = MIMEBase(mime_maintype, mime_subtype)
        part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={basename(file_path)}",
        )

        email_message.attach(part)

    text = email_message.as_string()

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, text)


def main():
    number = "18652094218"
    number1 = "18653231401"
    message = "I do not know why this is not getting through."
    provider = "T-Mobile"

    sender_credentials = ("kimanpark33@gmail.com", "byab pntv aygn eqbo")

    # SMS
    send_sms_via_email(number, message, provider, sender_credentials)
    send_sms_via_email(number1, message, provider, sender_credentials)
    '''
    # MMS
    file_path = "/path/to/file/file.png"

    mime_maintype = "image"
    mime_subtype = "png"

    send_mms_via_email(
        number,
        message,
        file_path,
        mime_maintype,
        mime_subtype,
        provider,
        sender_credentials,
    )
    '''

if __name__ == "__main__":
    main()






