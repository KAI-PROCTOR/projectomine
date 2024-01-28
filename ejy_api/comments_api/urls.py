from django.contrib import admin
from django.urls import path
from . import views
from .views import AddCommentView, PostCommentsView, DeleteCommentView





urlpatterns=[

    path('comments/add/', AddCommentView.as_view(), name='add-comment'),
path('comments/post/<int:post_id>/', PostCommentsView.as_view(), name='post-comments'),
path('comments/delete/<uuid:comment_id>/', DeleteCommentView.as_view(), name='delete-comment'),
]