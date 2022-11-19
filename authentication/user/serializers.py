from rest_framework import serializers
from authentication.profile.models import UserProfile
from authentication.user.models import User

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id',)


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        #profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
        )
        return user


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=278, required=False)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if not password:
            raise serializers.ValidationError(
                'Password field is required.'
            )
        if not email:
            raise serializers.ValidationError(
                'Email field is required.'
            )

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )

        try:
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'token': user.token,
            'email': email,
        }
