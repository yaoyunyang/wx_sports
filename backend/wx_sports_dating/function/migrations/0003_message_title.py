# Generated by Django 3.0.5 on 2020-04-18 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function', '0002_auto_20200414_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(default='[系统通知]', max_length=50),
        ),
    ]
