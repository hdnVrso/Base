from pw_reset_mail_sender.models.reset_pw_model import ResetPwModel
from authentication.models import User


class TokenChecker:
    def check_token(self, user_email, received_token, new_pw, r_new_pw):
        if ResetPwModel.objects.filter(userMail=user_email, token=received_token):
            user = User.objects.filter(email=user_email)
            if new_pw == r_new_pw:
                user.password = new_pw
                user.save()
                return "Password changed successfully", 200
            else:
                return "Password mismatch", 400
        else:
            return "invalid token", 403
