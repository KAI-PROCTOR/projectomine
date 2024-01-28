


from rest_framework.serializers import ModelSerializer
from django.utils import timezone

from datetime import datetime
from rest_framework import serializers




#USER SERIALIZERS 
    




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

    #
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






