# Generated by Django 2.0.2 on 2018-02-10 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0027_auto_20180210_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file_id',
            field=models.CharField(blank=True, default='9636306145135078404', max_length=200),
        ),
    ]