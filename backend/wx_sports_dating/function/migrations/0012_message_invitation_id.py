# Generated by Django 3.0.5 on 2020-04-30 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function', '0011_gym_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='invitation_id',
            field=models.IntegerField(default=0),
        ),
    ]