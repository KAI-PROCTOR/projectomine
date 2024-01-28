from django.db import models
# from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
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
    Blog=models.ManyToManyField('blog_api.Blog', related_name='users', blank=True)
    comments = models.ManyToManyField('comments_api.Comment', related_name='users', blank=True)
    savedblog= models.ManyToManyField('blog_api.Blog', related_name='saved_users', blank=True)
    @property
    def user_blogs(self):
        return self.blogs.all()

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName']

