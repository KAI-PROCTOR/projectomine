from django.db import models
# from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Customuser(AbstractBaseUser):
    ROLES = (
        ('User', 'User'),
        ('Content-Creator', 'Content-Creator'),
        ('Admin', 'Admin'),
        ('Moderator', 'Moderator'),
    )

    fullName = models.CharField(max_length=255)
    userId = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Assuming hashed password will be stored
    isEmailVerified = models.BooleanField(default=False)
    profilePic = models.URLField(blank=True, null=True)
    #roles = models.ManyToManyField(choices=ROLES, default='User', blank=True)
    roles = models.CharField(max_length=20, choices=ROLES, default='User', blank=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    Blog=models.ManyToManyField('Blog', related_name='users', blank=True)
    comments = models.ManyToManyField('Comment', related_name='users', blank=True)
    savedblog= models.ManyToManyField('Blog', related_name='saved_users', blank=True)
    @property
    def user_blogs(self):
        return self.blogs.all()

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName']








class Blog(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name='blogs')
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
    Blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='post_comments')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    def __str__(self):
        return f"{self.full_name} - {self.body}"































