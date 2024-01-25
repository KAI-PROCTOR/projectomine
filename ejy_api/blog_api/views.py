from django.shortcuts import render
from blog_api.serializer import BlogSerializer,ResetPasswordSerializer,DeleteBlogSerializer ,GetUserInfoSerializer,UserInfoSerializer,CommentSerializer,LikeBlogSerializer
from blog_api.serializer import BlogCreateSerializer ,LoginSerializer,LogoutSerializer,ForgotPasswordSerializer,ResetPasswordSerializer,ChangePasswordSerializer,EditProfileSerializer

#BlogCreateSerializer 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Blog, Comment
from .serializer import BlogSerializer, RegisterSerializer
from rest_framework.views import APIView
from .models import Customuser
from datetime import timedelta
from django.utils import timezone



#USER VIEWS 
#@api_view(['POST']) us this only for function based views not for class based.

class Registeruser(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Extract data from the validated serializer
            fullname = serializer.validated_data.get('fullname')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # Create a new user
            user = Customuser.objects.create_user(email=email, password=password, fullName=fullname)

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            access_token = serializer.validated_data.get('access_token')
            remember_me = serializer.validated_data.get('remember_me')

            if not remember_me:
                # If not remember_me, set token expiration to a short duration
                request.auth.expiry = timezone.now() + timedelta(minutes=15)

            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data.get('userId')

            # Perform logout operations (e.g., token revocation, session management)

            return Response({'message': f'User with ID {user_id} logged out successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.utils.crypto import get_random_string
from django.utils import timezone


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Generate a unique token for password reset
            reset_token = get_random_string(length=32)  # Adjust the length as needed

            # Store the reset token and its expiration in the user's profile
            user = Customuser.objects.get(email=email)
            user.reset_token = reset_token
            user.reset_token_expiry = timezone.now() + timezone.timedelta(minutes=15)  # Example: 15 minutes expiration
            user.save()

            # Simulate sending an email with the reset link containing the unique token
            reset_link = f'https://example.com/reset-password/?token={reset_token}'

            reset_link_sent_message = f'Reset link sent to {email}. Click the link to reset your password: {reset_link}'
            return Response({'message': reset_link_sent_message}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordview(APIView):
     def post(self, request, token):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data['password']
            confirmPassword = serializer.validated_data['confirmPassword']

            if password != confirmPassword:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Retrieve a user based on the provided token
                user = Customuser.objects.get(reset_token=token, reset_token_expiry__gt=timezone.now())

                # Reset the user's password
                user.set_password(password)
                user.save()

                # Clear the reset token and expiration
                user.reset_token = None
                user.reset_token_expiry = None
                user.save()

                return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)

            except Customuser.DoesNotExist:
                return Response({'error': 'Invalid or expired reset token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data['currentPassword']
            new_password = serializer.validated_data['newPassword']
            confirm_new_password = serializer.validated_data['confirmNewPassword']

            # Check if the new passwords match
            if new_password != confirm_new_password:
                return Response({'error': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the user making the request
            user = request.user

            # Check if the current password is valid
            if not user.check_password(current_password):
                return Response({'error': 'Invalid current password'}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfileView(APIView):
    def put(self, request):
        serializer = EditProfileSerializer(data=request.data)

        if serializer.is_valid():
            # Retrieve the user making the request
            user = request.user

            # Update the user's profile with the new email and full name
            new_email = serializer.validated_data.get('newEmail')
            new_full_name = serializer.validated_data.get('newFullName')

            if new_email:
                user.email = new_email
            if new_full_name:
                user.fullName = new_full_name

            user.save()

            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfoView(APIView):
    def get(self, request, id):
        try:
            user = Customuser.objects.get(id=id)
        except Customuser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        blogs = Blog.objects.filter(user=user)
        serializer = GetUserInfoSerializer({
            'fullName': user.fullName,
            'profilePic': user.profilePic,
            'blogs': BlogSerializer(blogs, many=True).data,
            'isEmailVerified': user.isEmailVerified,
            'roles': user.roles,
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
    

#●/user-info/:id : 
#○Request Type : POST
#○Response : email, fullName, roles, posts, comments, savedPosts, events, createdAt,profilePic,chat, isEmailVerified, (any other details)



#BLOG VIEWS 
@api_view(['GET'])
def all_blogs(request):
    all_posts = Blog.objects.all()
    serializer = BlogSerializer(all_posts, many=True)
    #many =true daala kyuki serializer ko batana tha ki kitne bhi 
    #queries laa sakte hai and not just one
    return Response(serializer.data)



class BlogCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        serializer = BlogCreateSerializer(data=request.data)

        if serializer.is_valid():
            # Extract data from the validated serializer
            title = serializer.validated_data.get('title')
            desc = serializer.validated_data.get('desc')
            body = serializer.validated_data.get('body')
            thumbnails = serializer.validated_data.get('thumbnails')
            keywords = serializer.validated_data.get('keywords')
            userId = serializer.validated_data.get('userId')

            # Create a new blog associated with the user
            user = request.user  # Assuming the user is authenticated
            blog = Blog.objects.create(
                user=user,
                title=title,
                desc=desc,
                body=body,
                thumbnails=thumbnails,
                keywords=keywords,
                userId=userId,
                url=f'{title}-{user.id}',  # Example: Title-UserID
            )

            return Response({'message': 'Blog created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, blog_id):
        serializer = DeleteBlogSerializer(data={'blog_id': blog_id})

        if serializer.is_valid():
            try:
                blog = Blog.objects.get(id=blog_id, user=request.user)
            except Blog.DoesNotExist:
                return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the user has permission to delete the blog
            user_role = request.user.roles
            if user_role not in ['Admin', 'Moderator'] and blog.user != request.user:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            # Perform the blog deletion
            blog.delete()
            return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializer import BlogDetailSerializer

class BlogDetailView(APIView):
    def get(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogDetailSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)



class LikeBlogView(APIView):
    def post(self, request, id):
        serializer = LikeBlogSerializer(data=request.data)

        if serializer.is_valid():
            try:
                blog = Blog.objects.get(id=id)
            except Blog.DoesNotExist:
                return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

            user_id = serializer.validated_data['userId']
            # Check if the user has already liked the blog
            if user_id in blog.likes['users']:
                return Response({'error': 'User has already liked the blog'}, status=status.HTTP_400_BAD_REQUEST)

            # Add the user to the list of likes and update the count
            blog.likes['users'].append(user_id)
            blog.likes['count'] += 1
            blog.save()

            return Response({'message': 'Blog liked successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











#comment views
class AddCommentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCommentsView(APIView):
    def get(self, request, post_id, *args, **kwargs):
        comments = Comment.objects.filter(Blog=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteCommentView(APIView):
    def delete(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)











  
















