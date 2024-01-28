

from .models import Customuser
from rest_framework.authtoken.models import Token







from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    userId = serializers.CharField(max_length=255)

    def validate_userId(self, value):
        # Check if the userId is unique
        if Customuser.objects.filter(userId=value).exists():
            raise serializers.ValidationError("This userId is already in use.")
        return value




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    rememberMe = serializers.BooleanField(default=False)
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Your custom authentication logic here
        user =Customuser.objects.filter(email=email).first()

        if user and user.check_password(password):
            # Generate or retrieve a token
            token, created = Token.objects.get_or_create(user=user)

            return {
                'user': user,
                'access_token': token.key,
                'remember_me': data.get('remember_me'),
            }

        raise serializers.ValidationError('Invalid email or password')



class LogoutSerializer(serializers.Serializer):
    userId = serializers.CharField(max_length=255)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()




class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)




class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True)
    confirmNewPassword = serializers.CharField(write_only=True)

class EditProfileSerializer(serializers.Serializer):
    newEmail = serializers.EmailField(required=False)
    newFullName = serializers.CharField(max_length=255, required=False)

class GetUserInfoSerializer(serializers.Serializer):
    fullName = serializers.CharField()
    profilePic = serializers.URLField()
    blogs = serializers.ListField(child=serializers.DictField(), source='user_blogs', read_only=True)
    isEmailVerified = serializers.BooleanField()
    roles = serializers.CharField()


class UserInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullName = serializers.CharField()
    roles = serializers.CharField()
    posts = serializers.IntegerField()
    comments = serializers.IntegerField()
    savedPosts = serializers.IntegerField()
    events = serializers.IntegerField()
    createdAt = serializers.DateTimeField()
    profilePic = serializers.URLField()
    chat = serializers.ListField()
    isEmailVerified = serializers.BooleanField()