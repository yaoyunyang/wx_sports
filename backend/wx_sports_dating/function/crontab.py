from . import models
import time
from django.core.cache import cache


def out_time_delete():
    datetime = time.strftime("%Y-%m-%d %H:%M", time.localtime()) + ':00'
    out_time = models.Invitation.objects.filter(end_time=datetime)
    if out_time:
        for item in out_time:
            print(datetime, ': delete the invitation ', item.id_invitation)
        out_time.delete()
    else:
        print(datetime, ': ======no out of date invitation======')
