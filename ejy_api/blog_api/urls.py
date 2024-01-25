from django.contrib import admin
from django.urls import path
from . import views
from blog_api.views import all_blogs,Registeruser,BlogCreateView,LoginView,LogoutView,AddCommentView, PostCommentsView, DeleteCommentView
from blog_api.views import ForgotPasswordView, ResetPasswordview, GetUserInfoView,DeleteBlogView,BlogDetailView, LikeBlogView,ChangePasswordView,EditProfileView


urlpatterns = [
    # path('',views.blogcreate,name='blogcreate'),
    
    path('create/',BlogCreateView.as_view(),name='blog_create'),
    path('registeruser/', Registeruser.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('reset-password/<str:token>/', ResetPasswordview.as_view(), name='reset-forgotten-password'),
    path('getinfouser/<int:id>/', GetUserInfoView.as_view(), name='get-user-info'),
    path('blogs/delete/<int:blog_id>/', DeleteBlogView.as_view(), name='delete-blog'),
    path('lists/',views.all_blogs,name='all_blogs'),
    path('detailblog/<int:id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('like/<int:id>/', LikeBlogView.as_view(), name='like-blog'),
    path('comments/add/', AddCommentView.as_view(), name='add-comment'),
    path('comments/post/<int:post_id>/', PostCommentsView.as_view(), name='post-comments'),
    path('comments/delete/<uuid:comment_id>/', DeleteCommentView.as_view(), name='delete-comment'),
    
    # path('list/',views.all_blog,name='list')
    
]
