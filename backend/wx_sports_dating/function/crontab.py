from . import models
import time
import datetime


def out_time_delete():
    current_time = time.strftime("%Y-%m-%d %H:%M", time.localtime()) + ':00'
    out_time = models.Invitation.objects.filter(end_time=current_time)
    if out_time:
        for item in out_time:
            print(datetime, ': delete the invitation ', item.id_invitation)
        out_time.delete()
    else:
        print(datetime, ': ======no out of date invitation======')


def statistic():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    last_year = (datetime.datetime.now() + datetime.timedelta(days=-14)).year
    last_month = (datetime.datetime.now() + datetime.timedelta(days=-14)).month
    last_date = (datetime.datetime.now() + datetime.timedelta(days=-14)).day
    gyms = models.Gym.objects.all()
    for gym in gyms:
        gym_id = gym.id_gym
        invitations = models.Invitation.objects.filter(
            gym_id_gym=gym_id, begin_time__gt=datetime.date(last_year, last_month, last_date))
        count_invitations = invitations.count()
        count_responder = 0
        for invitation in invitations:
            invitation_id = invitation.id_invitation
            count_responder += models.Responder.objects.filter(invitation_id_invitation=invitation_id).count()
        gym.count_invitation = count_invitations
        gym.count_responder = count_responder
        gym.save()
    print(current_time, ' : update count_invitations and count_responder for all gyms')