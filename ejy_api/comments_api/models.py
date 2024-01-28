from django.db import models
# from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from user_api.models import Customuser
from django.utils import timezone
from blog_api.models import Blog


# Create your models here.

class Comment(models.Model):
    STATUS_CHOICES = [
        ('waiting_for_approval', 'Waiting for Approval'),
        ('rejected', 'Rejected'),
        ('confirmed', 'Confirmed'),
        ('deleted', 'Deleted'),
        ('reported', 'Reported'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name='user_comments')
    Blog = models.ForeignKey('blog_api.Blog', on_delete=models.CASCADE, related_name='post_comments')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return f"{self.full_name} - {self.body}"
