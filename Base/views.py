from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


class Health(APIView):
    def head(self, request):
        return Response(status=200)
