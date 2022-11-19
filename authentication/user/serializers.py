from rest_framework import serializers
from authentication.profile.models import UserProfile
from authentication.user.models import User

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', )
        extra_kwargs = {'password': {'write_only': True, 'required': False}}


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        #profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        print(user)
        UserProfile.objects.create(
            user=user,
        )
        return user


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=278)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if password and not password == "null":
            user = authenticate(email=email, password=password)
        else:
            access_token = data.get("access_token", None)
            user = User.objects.get(
                email=email, access_token=access_token)

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
            'email': user.email,
        }
