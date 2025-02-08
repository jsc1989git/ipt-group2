# Generated by Django 5.1.4 on 2025-02-08 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_metadata_post_post_type_post_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('blog', 'Blog'), ('image', 'Image'), ('video', 'Video')], default='blog', max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
