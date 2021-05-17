from pw_reset_mail_sender.models.reset_pw_model import ResetPwModel
from authentication.models import User


class TokenChecker:
    def check_token(self, user_email, received_token, new_pw, r_new_pw):
        res_pw_model = ResetPwModel.objects.get(userMail=user_email)
        if res_pw_model.token == received_token:
            users = User.objects.filter(email=user_email)
            if new_pw == r_new_pw:
                for user in users:
                    user.password = new_pw
                    user.save()
                print(res_pw_model.delete())
                return "Password changed successfully", 200
            else:
                return "Password mismatch", 400
        else:
            print("hello")
            return "invalid token", 403
