import smtplib, ssl
from email.message import EmailMessage

    
def send_exp_outlook_email(reset_pwd,sender,receiver):
    port = 587  # For SSL
    smtp_server = 'localhost'
    msg = EmailMessage()
    msg['Subject'] = 'Reset your password'
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content('reset password: {pwd}'.format(pwd = reset_pwd))
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        #server.login(msg['From'], pwd)
        server.login(msg['From'], 'YOUR OUTLOOK LOGIN PASSWORD')
        server.send_message(msg)

