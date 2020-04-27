from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json, requests
from . import models
import time
import hashlib
from django.db.models import Q


# Create your views here.


def release_invitation(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        sports_type = data['sports_type']
        deadline = data['deadline']
        begin_time = data['begin_time']
        end_time = data['end_time']
        max_responsed = data['max_responsed']
        brif_introduction = data['brif_introduction']
        hash_id = data['hash_session']
        inviter_open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        gym_id_gym_id = models.Gym.objects.get(id_gym=data['id_gym'])
        inviter_id_account_id = models.Account.objects.get(open_id=inviter_open_id)

        invitation = models.Invitation(
            inviter_id_account=inviter_id_account_id,
            gym_id_gym=gym_id_gym_id,
            sports_type=sports_type,
            deadline=deadline,
            begin_time=begin_time,
            end_time=end_time,
            max_responsed=max_responsed,
            brif_introduction=brif_introduction,
            inviter_open_id=inviter_open_id
        )
        invitation.save()

        # 获取用户刚才创建的邀请ID， 即该用户的最新一条邀请
        invitation_id = models.Invitation.objects.filter(inviter_open_id=inviter_open_id).last().id_invitation
        response_data['invitation_id'] = invitation_id

        invite_list = data['selected_id']
        for invited in invite_list.split():
            account = models.Account.objects.get(id_account=int(invited))
            respond = models.Responder(
                invitation_id_invitation=invitation,
                account_id_account=account,
                state=0
            )
            respond.save()
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['msg'] = str(exception)
        response_data['status_code'] = 501

    return JsonResponse(response_data)


def get_my_follows(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        hash_id = data['hash_session']
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        followed_list = models.Follow.objects.filter(follower_open_id=open_id)
        follows = []
        for e in followed_list:
            id_account = e.followed_id
            follow_one = {}
            follow_one['name'] = models.Account.objects.filter(id_account=id_account).get().name
            follow_one['id'] = models.Account.objects.filter(id_account=id_account).get().id_account
            follow_one['avatar'] = models.Account.objects.filter(id_account=id_account).get().avatar
            follows.append(follow_one)
        response_data['followed_list'] = follows
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['msg'] = str(exception)
        response_data['status_code'] = 501
    return JsonResponse(response_data)


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
        # 'appid': 'wxe9e1e6704355a9ac',
        # 'secret': 'bcd537cb2b62e735d3c7f50dc6deb953',
        'appid': 'wx3c4f0e9741bd04e6',
        'secret': '7c6cfe909fc235de31e68f5584a9c44b',
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
        avatar = data['avatar']
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        is_exist = models.Account.objects.filter(open_id=open_id)
        if is_exist:
            account = models.Account.objects.get(open_id=open_id)
            account.name = name
            account.gender = gender
            account.avatar = avatar
            account.save()
        else:
            account = models.Account(
                open_id=open_id,
                name=name,
                gender=gender,
                avatar=avatar
            )
            account.save()
        response_data['name'] = account.name
        response_data['gender'] = account.gender
        response_data['profile'] = account.profile
        response_data['age'] = account.age
        response_data['favor_sports'] = account.favor_sports
        response_data['state'] = account.state
        response_data['avatar'] = account.avatar
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
        invitation_id = data['invitation_id']
        invitation = models.Invitation.objects.get(id_invitation=invitation_id)
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


def get_follows_list(request):
    follow_list = []
    response_data = {}
    try:
        data = json.loads(request.body)
        hash_id = data['hash_session']
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        followed_list = models.Follow.objects.filter(follower_open_id=open_id)
        for follow_one in followed_list:
            id_account = follow_one.followed_id
            follow_info = {'name': models.Account.objects.filter(id_account=id_account).get().name,
                           'avatar': models.Account.objects.filter(id_account=id_account).get().avatar,
                           'profile': models.Account.objects.filter(id_account=id_account).get().profile,
                           'age': models.Account.objects.filter(id_account=id_account).get().age,
                           'id': models.Account.objects.filter(id_account=id_account).get().id_account,
                           'state': models.Account.objects.filter(id_account=id_account).get().state,
                           'favor_sports': models.Account.objects.filter(id_account=id_account).get().favor_sports}
            follow_list.append(follow_info)
        response_data['follow_list'] = follow_list
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['status_code'] = 501
        response_data['msg'] = str(exception)
    return JsonResponse(response_data)


def respond_invitation(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        hash_id = data['hash_session']
        invitation_id = data['invitation_id']
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        account_id = models.Account.objects.filter(open_id=open_id).get().id_account
        invitation = models.Invitation.objects.filter(id_invitation=invitation_id).get()
        account = models.Account.objects.filter(open_id=open_id).get()
        has_respond = models.Responder.objects.filter(invitation_id_invitation=invitation_id,
                                                      account_id_account=account_id)
        if has_respond:
            response = is_respond.get()
            response.state = 1
            response.save()
        else:
            respond = models.Responder(
                invitation_id_invitation=invitation,
                account_id_account=account,
                state=1
            )
            respond.save()
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['status_code'] = 501
        response_data['msg'] = str(exception)
    return JsonResponse(response_data)


def is_respond(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        hash_id = data['hash_session']
        invitation_id = data['invitation_id']
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        account_id = models.Account.objects.filter(open_id=open_id).get().id_account
        invitation = models.Invitation.objects.filter(id_invitation=invitation_id).get()
        has_respond = models.Responder.objects.filter(invitation_id_invitation=invitation_id,
                                                      account_id_account=account_id)
        if has_respond:
            state = has_respond.get().state
            if state == 1:
                response_data['has_respond'] = 1
            else:
                response_data['has_respond'] = 0
        else:
            response_data['has_respond'] = 0
        has_respond_num = models.Responder.objects.filter(invitation_id_invitation=invitation_id).count()
        if has_respond_num < invitation.max_responsed:
            response_data['has_max'] = 0
        else:
            response_data['has_max'] = 1
        response_data['status_code'] = 200
    except Exception as exception:
        response_data['status_code'] = 501
        response_data['msg'] = str(exception)
    return JsonResponse(response_data)


def cancel_respond(request):
    response_data = {}
    try:
        data = json.loads(request.body)
        hash_id = data['hash_session']
        invitation_id = data['invitation_id']
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        account_id = models.Account.objects.filter(open_id=open_id).get().id_account
        is_delete = models.Responder.objects.get(invitation_id_invitation=invitation_id,
                                                 account_id_account=account_id).delete()
        if is_delete == 1:
            response_data['status_code'] = 200
            response_data['msg'] = '取消成功'
        else:
            response_data['status_code'] = 200
            response_data['msg'] = '取消失败'
    except Exception as exception:
        response_data['status_code'] = 501
        response_data['msg'] = str(exception)
    return JsonResponse(response_data)
