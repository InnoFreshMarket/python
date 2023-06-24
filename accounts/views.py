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


class InfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        serializer = UserInfoSerializer(User.objects.get(id=user_id))
        return Response(
            data={"info": serializer.data},
            status=201
        )

    def put(self, request, user_id):
        try:
            request.data._mutable = True
        except:
            pass
        if user_id != request.user.id:
            return Response(
                status=400
            )
        user = User.objects.get(id=user_id)
        request.data['email'] = user.email
        request.data['name'] = user.name
        serializer = UserInfoSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = User.objects.get(id=id)
        comments = user.comments.all()
        print(comments)
        serializer = CommentSerializer(comments, many=True)
        return Response(
            data={'comments': serializer.data},
            status=201
        )

    def post(self, request, id):
        user = User.objects.get(id=id)
        data = request.data
        comment = Comment.objects.create_comment(name=request.user.name,rate=data['rate'], text=data['text'])
        user.comments.add(comment)
        r = float(data['rate'])
        new_rate = (user.rate * user.numbers_of_comments + r) / (user.numbers_of_comments + 1)
        user.rate = new_rate
        user.numbers_of_comments += 1
        user.save()
        return Response(
            status=201
        )


class MyIdSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.user.id
        return Response(
            data={
                'id': id
            },
            status=200
        )