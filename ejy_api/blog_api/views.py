from django.shortcuts import render
from blog_api.serializer import BlogSerializer,DeleteBlogSerializer ,LikeBlogSerializer
from blog_api.serializer import BlogCreateSerializer 

#BlogCreateSerializer 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Blog
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone







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
            user = request.user  # Assuming the user is authenticated/role bhi daal idhar 
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
#role auth bhi daal .user role sab alag hoga.sirf content creator likes docs and staff can create blogs ..and admin .
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
# def  DeleteBlogView(self, request, blog_id):
#     serializer = DeleteBlogSerializer(data={'blog_id': blog_id})

#     if serializer.is_valid():
#         try:
#             blog = Blog.objects.get(id=blog_id, user=request.user)

#             # Check if the user has permission to delete the blog
#             user_role = request.user.roles
#             if user_role not in ['Admin', 'Moderator'] and blog.user != request.user:
#                 return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

#             # Perform the blog deletion
#             blog.delete()
#             return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_200_OK)

#         except Blog.DoesNotExist:
#             return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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


















  
















