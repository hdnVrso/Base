from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import configparser


class SmtpSender():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("mail_sender/config.ini")
        self.msg = MIMEMultipart()
        self.password = config['SMTP']['password']
        self.msg['From'] = config['SMTP']['mailer_email']
        self.server = smtplib.SMTP('smtp.yandex.ru: 587')
        self.server.starttls()

    def send_email(self, addressee, message):
        self.server.login(self.msg['From'], self.password)
        self.msg.attach(MIMEText(message, 'plain'))
        self.msg['To'] = addressee
        self.msg['Subject'] = "Сброс пароля BaseApp"
        self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        self.server.quit()
        return "successfully sent email to %s:" % (self.msg['To'])

# create server

# Login Credentials for sending the mail

# send the message via the server.
