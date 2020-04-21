from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from . import models


def get_account_info(request):
    response = {}
    try:
        open_id = request.GET.get('open_id')
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
        open_id = request.GET.get('open_id')
        my_invitation = models.Invitation.objects.filter(inviter_open_id=open_id)
        invite_me = models.Invitation.objects.filter()
        response['my_inv'] = json.loads(serializers.serialize("json", my_invitation))

        response['status'] = 200
    except Exception as exception:
        response['msg'] = str(exception)
        response['status'] = 501

    return JsonResponse(response)
