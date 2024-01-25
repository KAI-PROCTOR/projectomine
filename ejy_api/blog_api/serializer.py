
# class BlogSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     Title = serializers.CharField(max_length=100)
#     Desc = serializers.CharField(max_length=250)
#     Body = serializers.JSONField()
#     Url = serializers.CharField(max_length=255)
#     Status = serializers.ChoiceField(default='public', choices=[
#         ('public', 'Public'),
#         ('draft', 'Draft'),
#         ('private', 'Private'),
#         ('archived', 'Archived'),
#         ('deleted', 'Deleted'),
#         ('hold-for-validation', 'Hold for Validation')
#     ])
#     Thumbnail = serializers.URLField(default='https://image.com')
#     Likes = serializers.DictField(default=dict, allow_empty=True)
#     Views = serializers.IntegerField(default=0)
#     Tags = serializers.ListField(default=list, allow_empty=True)
#     Comments = serializers.ListField(default=list, allow_empty=True)
#     User = serializers.CharField(max_length=100) 
#     Category = serializers.ListField(default=list, allow_empty=True)
#     createdAt = serializers.DateTimeField(auto_now_add=True)
#     updatedAt = serializers.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.Url



from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token

from .models import Blog,Customuser,Comment

from rest_framework import serializers

from rest_framework import serializers
from .models import Blog



#USER SERIALIZERS 
    
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



#BLOG SERIALIZERS START


class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
     #id = models.AutoField(primary_key=True) for id = 1,2,3,4
    title = serializers.CharField(max_length=100)
    desc = serializers.CharField(max_length=250)
    body = serializers.JSONField()
    url = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=20)
    thumbnail = serializers.URLField()
    likes = serializers.JSONField()
    views = serializers.IntegerField()
    tags = serializers.JSONField()
    comments = serializers.JSONField()
    user = serializers.CharField(max_length=100)
    category = serializers.JSONField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert datetime fields to string representations
        data['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data['updated_at'] = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return data


   


from rest_framework import serializers

class BlogCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    desc = serializers.CharField(max_length=250)
    body = serializers.JSONField()
    thumbnails = serializers.URLField(default='https://image.com')
    keywords = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    userId = serializers.CharField(max_length=255)

    
class DeleteBlogSerializer(serializers.Serializer):
    blog_id = serializers.IntegerField()
    




class BlogDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    desc = serializers.CharField(max_length=250)
    body = serializers.JSONField()
    url = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=20)
    thumbnail = serializers.URLField()
    likes = serializers.JSONField()
    views = serializers.IntegerField()
    tags = serializers.JSONField()
    comments = serializers.JSONField()
    user = serializers.CharField(max_length=100)
    category = serializers.JSONField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert datetime fields to string representations
        data['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data['updated_at'] = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return data



class LikeBlogSerializer(serializers.Serializer):
    userId = serializers.CharField(max_length=255)







#comment serializer

from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'full_name', 'email', 'body', 'parent_comment', 'user', 'Blog', 'created_at', 'status']
