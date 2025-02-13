# Generated by Django 5.1.4 on 2025-02-13 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(blank=True, choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video')], max_length=10, null=True),
        ),
    ]
