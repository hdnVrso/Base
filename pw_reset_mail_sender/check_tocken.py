from pw_reset_mail_sender.models.reset_pw_model import ResetPwModel
from authentication.models import User


class TokenChecker:
    def check_token(self, user_email, received_token, new_password, new_password_rep):
        res_password_model = ResetPwModel.objects.get(userMail=user_email)
        if res_password_model.token == str(received_token):
            users = User.objects.filter(email=user_email)
            if new_password == new_password_rep:
                for user in users:
                    user.password = new_password
                    user.save()
                res_password_model.delete()
                return "Password changed successfully", 200
            else:
                return "Password mismatch", 400
        else:
            return "invalid token", 403
