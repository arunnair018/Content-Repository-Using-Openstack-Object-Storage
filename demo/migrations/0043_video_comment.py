# Generated by Django 2.0.2 on 2018-03-18 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0042_video_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='comment',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
