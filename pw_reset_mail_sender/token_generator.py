from uuid import uuid4
from authentication.models import User
from pw_reset_mail_sender.models.reset_pw_model import ResetPwModel
from pw_reset_mail_sender.smtp_sender import SmtpSender


class TokenGenerator:
    def check_email(self, user_email):
        return User.objects.filter(email=user_email).exists()

    def send_token(self, email):
        if self.check_email(email):
            rand_token = uuid4()
            new_reset = ResetPwModel(userMail=email, token=rand_token)
            new_reset.save()
            mail_sender = SmtpSender()
            message = str(rand_token) + "- Ваш код для восстановления пароля в приложении Base." + \
                      "\nЕсли вы не запрашивали данный код - просто проигнорируйте это письмо." + \
                      "\nС уважением,\nКоманда приложения Base."
            mail_sender.send_email(email, message, "Сброс пароля BaseApp")
            return True
        else:
            return False
