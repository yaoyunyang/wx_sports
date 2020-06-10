from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from . import models


def get_account_info(request):
    response = {}
    try:
        account_id = request.GET.get('account_id')
        account = models.Account.objects.filter(id_account=account_id)
        response['list'] = json.loads(serializers.serialize("json", account))
        response['status'] = 200
    except Exception as exception:
        response['msg'] = str(exception)
        response['status'] = 501

    return JsonResponse(response)


def get_notice(request):
    response = {}
    try:
        hash_id = request.GET.get('hash_session')
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        account = models.Account.objects.filter(open_id=open_id).first()
        my_invitation = models.Invitation.objects.filter(inviter_open_id=open_id)
        my_respond_list = models.Invitation.objects.filter(invitation__account_id_account=account)
        message = models.Message.objects.filter(receiver_id=account.id_account)
        my_respond = []
        message = models.Message.objects.filter(receiver_id=account.id_account)
        for invitation in my_invitation:
            invitation.inviter_state = len(invitation.invitation.all())
        for invitation in my_respond_list:
            respond = {}
            temp_account = models.Account.objects.filter(open_id=invitation.inviter_open_id).first()
            respond['inviter_state'] = len(invitation.invitation.all())
            respond['max_responsed'] = invitation.max_responsed
            respond['invitation_id'] = invitation.id_invitation
            respond['inviter_name'] = temp_account.name
            respond['inviter_avatar'] = temp_account.avatar
            respond['sports_type'] = invitation.sports_type
            respond['deadline'] = invitation.deadline
            my_respond.append(respond)
        response['my_inv'] = json.loads(serializers.serialize("json", my_invitation))
        response['my_respond'] = my_respond
        response['message'] = json.loads(serializers.serialize("json", message))
        response['status'] = 200
    except Exception as exception:
        response['msg'] = str(exception)
        response['status'] = 501

    return JsonResponse(response)
