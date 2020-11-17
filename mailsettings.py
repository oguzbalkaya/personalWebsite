import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from information import info


def SendMail(to,subject,text):
    mesaj = MIMEMultipart()
    mesaj["From"] = info["from"]
    mesaj["To"] = to
    mesaj["Subject"] = subject
    mesaj_govdesi = MIMEText(text,"html")
    mesaj.attach(mesaj_govdesi)
    mail = smtplib.SMTP(info["smtp_server"],info["smtp_port"])
    mail.ehlo()
    mail.starttls()
    mail.login(info["smtp_username"],info["smtp_password"])
    mail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
