from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from . import models


# Create your views here.


def release_invitation(request):
    data = json.loads(request.body)
    sports_type = data['sports_type']
    deadline = data['deadline']
    begin_time = data['begin_time']
    end_time = data['end_time']
    max_responsed = data['max_responsed']
    brif_introduction = data['brif_introduction']
    state = data['state']
    inviter_state = data['inviter_state']
    inviter_open_id = data['open_id']
    gym_id_gym_id = models.Gym.objects.get(id_gym=data['id_gym'])
    inviter_id_account_id = models.Account.objects.get(open_id=data['open_id'])

    invitation = models.Invitation(
        inviter_id_account=inviter_id_account_id,
        gym_id_gym=gym_id_gym_id,
        sports_type=sports_type,
        deadline=deadline,
        begin_time=begin_time,
        end_time=end_time,
        max_responsed=max_responsed,
        brif_introduction=brif_introduction,
        state=state,
        inviter_state=inviter_state,
        inviter_open_id=inviter_open_id
    )
    invitation.save()

    # 获取用户刚才创建的邀请ID， 即该用户的最新一条邀请
    invitation_id = models.Invitation.objects.filter(inviter_open_id='asdf123').last().id_invitation

    response_data = {
        "invitation_id": invitation_id,
    }
    return JsonResponse(response_data)
