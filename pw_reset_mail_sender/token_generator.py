from uuid import uuid4
from authentication.models import User
from pw_reset_mail_sender.models.reset_pw_model import ResetPwModel
from pw_reset_mail_sender.smtp_sender import SmtpSender


class TokenGenerator:
    def check_email(self, user_email):
        return User.objects.filter(email=user_email).exists()

    def send_token(self, email):
        if self.check_email(email):
            new_token = uuid4()
            new_reset = ResetPwModel(userMail=email, token=new_token)
            new_reset.save()
            mail_sender = SmtpSender()
            text = "- Ваш код для восстановления пароля в приложении Base." + \
                   "\nЕсли вы не запрашивали данный код - просто проигнорируйте это письмо." + \
                   "\nС уважением,\nКоманда приложения Base."
            message = str(new_token) + text
            mail_sender.send_email(email, message, "Сброс пароля BaseApp")
            return True
        else:
            return False
