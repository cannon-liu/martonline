# Generated by Django 2.0.6 on 2018-08-09 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verifycode',
            options={'verbose_name': '验证码', 'verbose_name_plural': '验证码'},
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='add_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='添加时间'),
        ),
    ]
