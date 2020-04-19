# Generated by Django 3.0.5 on 2020-04-19 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function', '0004_auto_20200419_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_id', models.CharField(max_length=50)),
                ('session_key', models.CharField(max_length=50)),
                ('hash_id', models.CharField(max_length=50)),
                ('login_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
