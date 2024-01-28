# Generated by Django 4.2.5 on 2024-01-28 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0005_remove_comment_blog_remove_comment_parent_comment_and_more'),
        ('user_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to='user_api.customuser'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Customuser',
        ),
    ]