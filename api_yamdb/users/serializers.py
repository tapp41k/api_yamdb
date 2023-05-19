from rest_framework import serializers

from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=149)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=149)
    confirmation_code = serializers.CharField(required=True, max_length=40)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User
