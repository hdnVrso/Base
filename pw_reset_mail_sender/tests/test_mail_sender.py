from django.test import TestCase
from pw_reset_mail_sender.models.reset_pw_model import ResetPwModel
from pw_reset_mail_sender.check_tocken import TokenChecker
from pw_reset_mail_sender.token_generator import TokenGenerator
from pw_reset_mail_sender.smtp_sender import SmtpSender
from uuid import uuid4
import threading
import datetime
import time
from authentication.models import User
import subprocess


class TestMailSender(TestCase):
    def create_debugging_server(self):
        command = ['python -m smtpd -n -c DebuggingServer 127.0.0.1:1025']
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def test_check_token_wrong_token(self):
        email = "user_email@mail.mail"
        token_to_send = uuid4()
        invalid_token = uuid4()
        new_reset = ResetPwModel(userMail=email, token=token_to_send)
        new_reset.save()
        check_code = TokenChecker()
        response = check_code.check_token(email, invalid_token, "pw123456", "pw123456")
        self.assertEqual(response[1], 403)

    def test_check_token(self):
        email = "user_email1@mail.mail"
        token = uuid4()
        user = User(email='email@email.com', username='use1214',
                    password='Pass1234')
        user.save()
        new_reset = ResetPwModel(userMail=email, token=token)
        new_reset.save()
        check_code = TokenChecker()
        response = check_code.check_token(email, token, "pw123456", "pw123456")

        self.assertEqual(response[1], 200)

    def test_check_email(self):
        user_email = 'user@email.com'
        user = User(email=user_email, username='use1214',
                    password='Pass1234')
        user.save()
        token_generator = TokenGenerator()
        self.assertTrue(token_generator.check_email(user_email))

    def test_send_email(self):
        x = threading.Thread(target=self.create_debugging_server)
        x.daemon = True  # This thread dies when main thread (only non-daemon thread) exits.
        x.start()
        time.sleep(2)
        sender = SmtpSender()
        sender.send_email("my@me.muuu", "hello", "autotest" + str(datetime.datetime.now()))
        if sender:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_check_wrong_email(self):
        email = "user_email3@mail.mail"
        token_generator = TokenGenerator()
        self.assertFalse(token_generator.check_email(email))

    def test_create_new_reset(self):
        x = threading.Thread(target=self.create_debugging_server)
        x.daemon = True
        x.start()
        time.sleep(2)
        user_email = 'user@email.com'
        user = User(email=user_email, username='use1214',
                    password='Pass1234')
        user.save()
        token_generator = TokenGenerator()
        token_generator.send_token(user_email)
        self.assertTrue(ResetPwModel.objects.filter(userMail=user_email).exists())
