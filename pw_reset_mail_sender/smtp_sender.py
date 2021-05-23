from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from Base import settings


class SmtpSender:
    def __init__(self):
        self.msg = MIMEMultipart()
        self.password = settings.MAIL_PASSWORD
        self.msg['From'] = settings.MAIL_ADR
        host_and_port = settings.EMAIL_HOST + ': ' + str(settings.EMAIL_PORT)
        self.server = smtplib.SMTP(host_and_port)
        if not settings.DEBUG:
            self.server.starttls()
            self.server.login(self.msg['From'], self.password)

    def send_email(self, addressee, message, subject):
        self.msg.attach(MIMEText(message, 'plain'))
        self.msg['To'] = addressee
        self.msg['Subject'] = subject
        self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        self.server.quit()
        return "successfully sent email to %s:" % (self.msg['To'])
