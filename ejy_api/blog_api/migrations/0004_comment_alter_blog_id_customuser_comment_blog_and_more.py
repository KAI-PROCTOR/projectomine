# Generated by Django 4.2.5 on 2024-01-24 16:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0003_rename_body_blog_body_rename_category_blog_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('waiting_for_approval', 'Waiting for Approval'), ('rejected', 'Rejected'), ('confirmed', 'Confirmed'), ('deleted', 'Deleted'), ('reported', 'Reported')], default='confirmed', max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Customuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('fullName', models.CharField(max_length=255)),
                ('userId', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('isEmailVerified', models.BooleanField(default=False)),
                ('profilePic', models.URLField(blank=True, null=True)),
                ('roles', models.CharField(blank=True, choices=[('User', 'User'), ('Content-Creator', 'Content-Creator'), ('Admin', 'Admin'), ('Moderator', 'Moderator')], default='User', max_length=20)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('Blog', models.ManyToManyField(blank=True, related_name='users', to='blog_api.blog')),
                ('comments', models.ManyToManyField(blank=True, related_name='users', to='blog_api.comment')),
                ('savedblog', models.ManyToManyField(blank=True, related_name='saved_users', to='blog_api.blog')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='Blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='blog_api.blog'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog_api.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='blog_api.customuser'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to='blog_api.customuser'),
        ),
    ]
