from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from . import models


def get_account_info(request):
    response = {}
    try:
        hash_id = request.GET.get('hash_session')
        open_id = models.Login.objects.filter(hash_id=hash_id).last().open_id
        account = models.Account.objects.filter(open_id=open_id).first()
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
        invite_me = models.Invitation.objects.filter(invitation__account_id_account=account)
        message = models.Message.objects.filter(receiver_id=open_id)
        response['my_inv'] = json.loads(serializers.serialize("json", my_invitation))
        response['inv_me'] = json.loads(serializers.serialize("json", invite_me))
        response['message'] = json.loads(serializers.serialize("json", message))
        response['status'] = 200
    except Exception as exception:
        response['msg'] = str(exception)
        response['status'] = 501

    return JsonResponse(response)
