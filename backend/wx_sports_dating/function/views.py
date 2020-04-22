from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json, requests
from . import models
import time
import hashlib
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
    response_data = {
        "status_code": 200
    }
    return JsonResponse(response_data)


def send_message(request):
    data = json.loads(request.body)
    receiver_id = data['receiver_open_id']
    content = data['content']
    sender_id = data['sender_open_id']
    state = data['state']
    type = data['type']
    title = data['title']
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    message = models.Message(
        content=content,
        datetime=datetime,
        type=type,
        state=state,
        receiver_id=receiver_id,
        sender_id=sender_id,
        title=title
    )
    message.save()
    response_data = {
        "status_code": 200
    }

    return JsonResponse(response_data)


def gym_is_exist(request):
    data = json.loads(request.body)
    longitude = data['longitude']
    latitude = data['latitude']
    is_exist = models.Gym.objects.filter(longitude=longitude, latitude=latitude)
    if is_exist:
        gym = models.Gym.objects.filter(longitude=longitude, latitude=latitude).last()
        response_data = {
            "status_code": 200,
            "gym_info": {
                "p_key": gym.id_gym,
                "name": gym.name,
                "heat": gym.heat,
                "charge": gym.charge,
                "peak_time": gym.peak_time,
                "time": gym.time,
                "brief_introduction": gym.brief_introduction
            }
        }
    else:
        status_code = 501
        response_data = {
            "status_code": status_code
        }

    return JsonResponse(response_data)


def login(request):
    js_code = request.GET.get('code')
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    # 需要更改为前端的appid 和 secret
    params = {
        'appid': 'wxe9e1e6704355a9ac',
        'secret': 'bcd537cb2b62e735d3c7f50dc6deb953',
        'js_code': js_code,
        'grant_type': 'authorization_code'
    }

    response = requests.get(url=url, params=params)
    if response.json()['session_key']:
        print(response.json())
        md5 = hashlib.md5()
        open_id = response.json()['openid']
        session_key = response.json()['session_key']
        hash_str = open_id + session_key
        md5.update(hash_str.encode('utf-8'))
        login = models.Login(
            open_id=open_id,
            session_key=session_key,
            hash_id=md5.hexdigest()
        )
        login.save()
        response_data = {
            'hash_session': md5.hexdigest()
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'status_code': 501
        }

        return JsonResponse(response_data)


def store_info(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        hash_id = data['hash_session']
        name = data['name']
        gender = data['gender']
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        is_exist = models.Account.objects.filter(open_id=open_id)
        if is_exist:
            account = models.Account.objects.get(open_id=open_id)
            account.name = name
            account.gender = gender
            account.save()
        else:
            account = models.Account(
                open_id=open_id,
                name=name,
                gender=gender,
            )
            account.save()
        response_data['name'] = account.name
        response_data['gender'] = account.gender
        response_data['profile'] = account.profile
        response_data['age'] = account.age
        response_data['favor_sports'] = account.favor_sports
        response_data['state'] = account.state
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['msg'] = str(exception)
        response_data['status_code'] = 501

    return JsonResponse(response_data)


def modify_info(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        age = data['age']
        profile = data['profile']
        hash_id = data['hash_session']
        favor_sports = data['favor_sports']
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        account = models.Account.objects.get(open_id=open_id)
        account.age = age
        account.profile = profile
        account.favor_sports = favor_sports
        account.save()
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['msg'] = str(exception)
        response_data['status_code'] = 501

    return JsonResponse(response_data)


def respond_list(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        gym_id = data['gym_id']
        invitations_list = []
        invitations = models.Invitation.objects.filter(gym_id_gym_id=gym_id)
        for invitation in invitations:
            invitation_dic = {}
            invitation_dic['invitation_id'] = invitation.id_invitation
            invitation_dic['sports_type'] = invitation.sports_type
            invitation_dic['begin_time'] = invitation.begin_time
            invitation_dic['max_responsed'] = invitation.max_responsed
            inviter_name = models.Account.objects.filter(open_id=invitation.inviter_open_id).get().name
            invitation_dic['inviter_name'] = inviter_name
            has_respond = len(invitation.invitation.all())
            invitation_dic['has_respond'] = has_respond
            invitations_list.append(invitation_dic)
        response_data['invitation_list'] = invitations_list
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['status_code'] = 501
        response_data['msg'] = str(exception)
    return JsonResponse(response_data)


def get_invite_detail(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        invtation_id = data['invtation_id']
        invitation = models.Invitation.objects.get(id_invitation=invtation_id)
        invitation_dic = {}
        invited_list = []
        invited_one = {}
        invitation_dic['state'] = invitation.state
        invitation_dic['sports_type'] = invitation.sports_type
        invitation_dic['inviter_state'] = invitation.inviter_state
        invitation_dic['brif_introduction'] = invitation.brif_introduction
        invitation_dic['deadline'] = invitation.deadline
        invitation_dic['begin_time'] = invitation.begin_time
        invitation_dic['end_time'] = invitation.end_time
        invitation_dic['max_responsed'] = invitation.max_responsed
        inviter_name = models.Account.objects.filter(open_id=invitation.inviter_open_id).get().name
        invitation_dic['inviter_name'] = inviter_name
        has_respond = len(invitation.invitation.all())
        for item in invitation.invitation.all():
            account = models.Account.objects.filter(id_account=item.account_id_account_id).get()
            invited_one['name'] = account.name
            invited_list.append(invited_one)
        invitation_dic['has_respond'] = has_respond
        invitation_dic['invited_list'] = invited_list
        response_data['detail'] = invitation_dic
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['msg'] = str(exception)
        response_data['status_code'] = 501
    return JsonResponse(response_data)
