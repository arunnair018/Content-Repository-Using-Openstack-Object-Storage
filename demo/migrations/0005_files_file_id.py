# Generated by Django 2.0.2 on 2018-02-10 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0004_remove_files_file_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='file_id',
            field=models.IntegerField(default=153134856178474482628791112672240424679),
        ),
    ]