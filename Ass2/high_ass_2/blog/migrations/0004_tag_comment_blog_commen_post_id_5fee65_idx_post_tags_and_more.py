# Generated by Django 5.1.1 on 2024-10-11 07:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['post', 'created_at'], name='blog_commen_post_id_5fee65_idx'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='blog.tag'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author'], name='blog_post_author__038a48_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['created_at'], name='blog_post_created_b20a1e_idx'),
        ),
    ]
