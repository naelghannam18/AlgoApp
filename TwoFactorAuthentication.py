import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def sendVerificationCode(destEmail, code):
    senderEmail = '[Enter Email Here]'
    senderPassword = '[Enter Email Password]'
    receiverEmail = destEmail
    body = f"You have logged in to AlgoApp. Please Use Below Code to complete Verification.\n\nCode: {code}"
    message=MIMEMultipart()
    message['From'] = senderEmail
    message['To'] = receiverEmail
    message['Subject'] = "First Level 2-Factor Authentication."

    message.attach(MIMEText(body, 'plain'))

    session = smtplib.SMTP('smtp.office365.com', 587)
    session.ehlo()
    session.starttls()
    session.login(senderEmail, senderPassword)
    email = message.as_string()
    session.sendmail(senderEmail, receiverEmail, email)
    session.quit()

def sendUnAuthorizedEmail(destEmail):
    senderEmail = '[Enter Email Here]'
    senderPassword = '[Enter Email Password here]'
    receiverEmail = destEmail
    body = "An Unauthorized Access Was Attempted On Your Application.\n"
    body+= "You Are Required To Change Your Credentials Immediately\n"
    timeNow = str (datetime.datetime.now ().strftime ("%I:%M%p on %B %d, %Y"))
    body+= f"\nLogin Time: {timeNow}"
    message = MIMEMultipart ()
    message['From'] = senderEmail
    message['To'] = receiverEmail
    message['Subject'] = "Security Breach"

    message.attach (MIMEText (body, 'plain'))

    session = smtplib.SMTP ('smtp.office365.com', 587)
    session.ehlo ()
    session.starttls ()
    session.login (senderEmail, senderPassword)
    email = message.as_string ()
    session.sendmail (senderEmail, receiverEmail, email)
    session.quit ()








