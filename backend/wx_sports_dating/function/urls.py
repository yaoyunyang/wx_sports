from django.urls import path
from . import views
from . import views1

urlpatterns = [
    path('release', views.release_invitation),
    path('my_follows', views.get_my_follows),
    path('evaluate_gym', views.evaluate_gym),
    path('send_message', views.send_message),
    path('gym_is_exist', views.gym_is_exist),
    path('get_account_info', views1.get_account_info),
    path('get_notice', views1.get_notice),
    path('gym_is_exist', views.gym_is_exist),
    path('login', views.login),
    path('store_info', views.store_info),
    path('modify_info', views.modify_info),
    path('respond_list', views.respond_list),
    path('get_invite_detail', views.get_invite_detail),
    path('get_follows_list', views.get_follows_list),
    path('respond_invitation', views.respond_invitation),
    path('is_respond', views.is_respond),
    path('cancel_respond', views.cancel_respond),
    path('add_friends', views.add_friends),
    path('delete_friends', views.delete_friends),
    path('is_sponsor', views.is_sponsor),
    path('delete_invitation', views.delete_invitation),
    path('clock_in', views.clock_in),
    path('is_clock_in', views.is_clock_in)
]
