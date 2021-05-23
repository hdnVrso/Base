from rest_framework.views import APIView
from rest_framework.response import Response


class Health(APIView):
    def head(self, request):
        return Response(status=200)
