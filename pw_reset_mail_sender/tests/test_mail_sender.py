from django.test import TestCase
from pw_reset_mail_sender.models.reset_pw_model import ResetPwModel
from pw_reset_mail_sender.check_tocken import TokenChecker
from pw_reset_mail_sender.token_generator import TokenGenerator
from uuid import uuid4
from authentication.models import User


class TestMailSender(TestCase):
    def test_check_token_wrong_token(self):
        email = "user_email@mail.mail"
        token1 = uuid4()
        token2 = uuid4()
        new_reset = ResetPwModel(userMail=email, token=token1)
        new_reset.save()
        chk_code = TokenChecker()
        response = chk_code.check_token(email, token2, "pw123456", "pw123456")
        if response[1] == 403:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_check_token(self):
        email = "user_email1@mail.mail"
        token = uuid4()
        user = User(email='email@email.com', username='use1214',
                    password='Pass1234')
        user.save()
        new_reset = ResetPwModel(userMail=email, token=token)
        new_reset.save()
        chk_code = TokenChecker()
        response = chk_code.check_token(email, token, "pw123456", "pw123456")
        if response[1] == 200:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
    def test_check_email(self):
        user_email = 'user@email.com'
        user = User(email=user_email, username='use1214',
                    password='Pass1234')
        user.save()
        tg = TokenGenerator()
        if tg.check_email(user_email):
            self.assertTrue(True)
        else:
            self.assertTrue(False)



