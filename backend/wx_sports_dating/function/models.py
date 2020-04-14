from django.db import models

# Create your models here.


class Account(models.Model):
    id_account = models.AutoField(primary_key=True)
    open_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    gender = models.IntegerField(default=0, blank=True)
    age = models.IntegerField(default=0)
    profile = models.CharField(max_length=255, blank=True)
    state = models.IntegerField(default=0)


class Invitation(models.Model):
    id_invitation = models.AutoField(primary_key=True)
    inviter_id_account = models.ForeignKey('Account', on_delete=models.CASCADE)
    inviter_open_id = models.CharField(max_length=50)
    gym_id_gym = models.ForeignKey('Gym', on_delete=models.CASCADE)
    sports_type = models.IntegerField()
    deadline = models.DateTimeField()
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_responsed = models.IntegerField()
    brif_introduction = models.CharField(max_length=255)
    state = models.IntegerField()
    inviter_state = models.IntegerField()


class Gym(models.Model):
    id_gym = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    heat = models.IntegerField(default=100, blank=True)
    time = models.CharField(max_length=50, blank=True)
    charge = models.CharField(max_length=50, blank=True)
    peak_time = models.CharField(max_length=50, default='16:00-18:00', blank=True)


class Message(models.Model):
    id_message = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    type = models.IntegerField()
    state = models.IntegerField()
    receiver_id = models.CharField(max_length=50)
    sender_id = models.CharField(max_length=50)


class GymComment(models.Model):
    id_gym_comment = models.AutoField(primary_key=True)
    account_id_account = models.ForeignKey('Account', on_delete=models.CASCADE)
    gym_id_gym = models.ForeignKey('Gym', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)


class Follow(models.Model):
    id_follow = models.AutoField(primary_key=True)
    follower = models.ForeignKey('Account', related_name='follower_account', on_delete=models.CASCADE)
    followed = models.ForeignKey('Account',  related_name='followed_account',on_delete=models.CASCADE)
    invite_num = models.IntegerField()


class Responder(models.Model):
    id_responder = models.AutoField(primary_key=True)
    invitation_id_invitation = models.ForeignKey('Invitation', on_delete=models.CASCADE)
    account_id_account = models.ForeignKey('Account', on_delete=models.CASCADE)
    state = models.IntegerField()