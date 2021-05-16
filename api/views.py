from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import RequestSerializer



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
        return Response("Not implemented", status=500)