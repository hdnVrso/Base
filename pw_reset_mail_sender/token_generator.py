from uuid import uuid4
from authentication.models import User
from pw_reset_mail_sender.models.reset_pw_model import ResetPwModel
from pw_reset_mail_sender.smtp_sender import SmtpSender


class TokenGenerator:
    def chek_email(self, user_email):
        if User.objects.filter(email=user_email):
            return True
        else:
            return False

    def send_token(self, email):
        if self.check_email:
            rand_token = uuid4()
            new_reset = ResetPwModel(userMail=email, token=rand_token)
            new_reset.save()
            mail_sender = SmtpSender()
            mail_sender.send_email(email, rand_token)
            return True
        else:
            return False
