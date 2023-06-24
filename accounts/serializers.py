import os

from django.contrib.auth import authenticate

from .models import *
import base64
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    # username = serializers.CharField()
    # password = serializers.CharField()
    class Meta:
        model = User
        fields = ['name', 'password', 'email', 'role']
        write_only_fields = ['password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['name'] = self.user.name
        data['role'] = self.user.role
        data['id'] = self.user.id
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.card = validated_data.get('card', instance.card)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['email', 'name', 'role', 'address', 'phone_number', 'card', 'rate']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'rate', 'text', 'date']

    def create(self, validated_data):
        item = Item.objects.create(
            **validated_data
        )

        return item