from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from django.core import serializers
import base64
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenViewBase

from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def me(self, request):
        return Response(
            data=UserSerializer(request.user).data
        )


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            data={
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=201
        )


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer