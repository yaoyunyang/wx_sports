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
    invitation_id = models.Invitation.objects.filter(inviter_open_id=inviter_open_id).last().id_invitation

    response_data = {
        "invitation_id": invitation_id
    }
    return JsonResponse(response_data)


def get_my_follows(request):
    data = json.loads(request.body)
    open_id = data['open_id']
    followed_list = models.Follow.objects.filter(follower_open_id=open_id)
    response_data = []
    for e in followed_list:
        id_account = e.followed_id
        account_info = list(models.Account.objects.filter(id_account=id_account).values())
        response_data.extend(account_info)
    print(response_data)
    return JsonResponse(response_data, safe=False)


def evaluate_gym(request):
    data = json.loads(request.body)
    open_id = data['open_id']
    account_id_account = models.Account.objects.get(open_id=open_id)
    comment = data['comment']
    gym_id_gym = models.Gym.objects.get(id_gym=data['id_gym'])
    gym_comment = models.GymComment(
        account_id_account=account_id_account,
        gym_id_gym=gym_id_gym,
        comment=comment
    )
    gym_comment.save()
    response_data={
        "state_code": 200
    }
    return JsonResponse(response_data)
