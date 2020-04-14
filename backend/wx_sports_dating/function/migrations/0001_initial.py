# Generated by Django 3.0.5 on 2020-04-14 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id_account', models.AutoField(primary_key=True, serialize=False)),
                ('open_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.IntegerField(blank=True, default=0)),
                ('age', models.IntegerField(default=0)),
                ('profile', models.CharField(blank=True, max_length=255)),
                ('state', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id_gym', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('heat', models.IntegerField(blank=True, default=100)),
                ('time', models.CharField(blank=True, max_length=50)),
                ('charge', models.CharField(blank=True, max_length=50)),
                ('peak_time', models.CharField(blank=True, default='16:00-18:00', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id_invitation', models.AutoField(primary_key=True, serialize=False)),
                ('inviter_open_id', models.CharField(max_length=50)),
                ('sports_type', models.IntegerField()),
                ('deadline', models.DateTimeField()),
                ('begin_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('max_responsed', models.IntegerField()),
                ('brif_introduction', models.CharField(max_length=255)),
                ('state', models.IntegerField()),
                ('inviter_state', models.IntegerField()),
                ('gym_id_gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='function.Gym')),
                ('inviter_id_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='function.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id_message', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('type', models.IntegerField()),
                ('state', models.IntegerField()),
                ('receiver_id', models.CharField(max_length=50)),
                ('sender_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Responder',
            fields=[
                ('id_responder', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.IntegerField()),
                ('account_id_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='function.Account')),
                ('invitation_id_invitation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='function.Invitation')),
            ],
        ),
        migrations.CreateModel(
            name='GymComment',
            fields=[
                ('id_gym_comment', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=255)),
                ('account_id_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='function.Account')),
                ('gym_id_gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='function.Gym')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id_follow', models.AutoField(primary_key=True, serialize=False)),
                ('invite_num', models.IntegerField()),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_account', to='function.Account')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_account', to='function.Account')),
            ],
        ),
    ]
