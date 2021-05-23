from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer
from .serializers import AccessTokensSerializer
from .backends import JWTRefreshAuthentication

from .renderers import UserJSONRenderer


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer, )

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ObtainTokenAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = AccessTokensSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RefreshTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    authentication_classes = (JWTRefreshAuthentication, )

    def post(self, request):
        response = {
            'email': request.user.email,
            'username': request.user.username,
            'access_token': request.user.access_token,
            'refresh_token': request.user.refresh_token
        }

        return Response(data=response, status=status.HTTP_200_OK)
