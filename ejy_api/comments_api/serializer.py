



from rest_framework import serializers





#comment serializer

from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'full_name', 'email', 'body', 'parent_comment', 'user', 'Blog', 'created_at', 'status']
