from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import RequestSerializer
from pw_reset_mail_sender.check_tocken import TokenChecker
from pw_reset_mail_sender.token_generator import TokenGenerator


class Health(APIView):
    def head(self, request):
        return Response(status=200)


class Users(APIView):
    def get(self, request: Request):
        return Response("Not implemented", status=500)

    def post(self, request: Request):
        return Response("Not implemented", status=500)

    def put(self, request: Request):
        return Response("Not implemented", status=500)

    def delete(self, requet: Request):
        return Response("Not implemented", status=500)


class Requests(APIView):
    def post(self, request: Request):
        serialized_request = RequestSerializer(data=request)
        serialized_request.is_valid(raise_exception=True)
        return Response("Not implemented", status=500,
                        content_type='application/json')


class RequestsHistory(APIView):
    def get(self, request: Request):
        return Response("Not implemented", status=500)


class RequestsRating(APIView):
    def get(self, request: Request):
        return Response("Not implemented", status=500)


class ResetPassword(APIView):
    def post(self, request: Request):
        email = request.data.get('email', {})
        token = request.data.get('token', {})
        new_password = request.data.get('new_password', {})
        repeated_new_password = request.data.get('new_password1', {})
        check_token = TokenChecker()
        resp = check_token.check_token(email, token, new_password, repeated_new_password)
        return Response(resp[1], status=resp[2])


class SetEmail(APIView):
    def post(self, request: Request):
        email = request.data.get('email', {})
        token_gen = TokenGenerator()
        res = token_gen.send_token(email)
        if res:
            return Response("Token sent successfully", status=200)
        else:
            return Response("No user with this email address", status=403)
