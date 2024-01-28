from django.contrib import admin
from django.urls import path
from . import views
from blog_api.views import all_blogs,BlogCreateView
from blog_api.views import DeleteBlogView,BlogDetailView, LikeBlogView


urlpatterns = [
    # path('',views.blogcreate,name='blogcreate'),
    
    path('create/',BlogCreateView.as_view(),name='blog_create'),
    path('blogs/delete/<int:blog_id>/', DeleteBlogView.as_view(), name='delete-blog'),
    path('lists/',views.all_blogs,name='all_blogs'),
    path('detailblog/<int:id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('like/<int:id>/', LikeBlogView.as_view(), name='like-blog'),
]
