from django.db import models
# from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
# from user_api.models import Customuser
from django.utils import timezone



class Blog(models.Model):
    user = models.ForeignKey('user_api.Customuser', on_delete=models.CASCADE, related_name='blogs')
    # access the blogs associated with a user using my_user.blogs.all()
    id = models.AutoField(primary_key=True) 
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=250)
    body = models.JSONField()
    url = models.CharField(max_length=255, unique=True)
    status = models.JSONField(default=list, choices=[
        ('public', 'Public'),
        ('draft', 'Draft'),
        ('private', 'Private'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
        ('hold-for-validation', 'Hold for Validation')
    ])
    thumbnail = models.URLField(default='https://image.com')
    likes = models.JSONField(default=dict, blank=True)
    views = models.IntegerField(default=0)
    tags = models.JSONField(default=list, blank=True)
    comments = models.JSONField(default=list)
    category = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


































