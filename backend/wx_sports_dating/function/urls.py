from django.urls import path
from . import views

urlpatterns = [
    path('release', views.release_invitation),
    path('my_follows', views.get_my_follows),
    path('evaluate_gym', views.evaluate_gym),
    path('send_message', views.send_message),
    path('gym_is_exist', views.gym_is_exist),
    path('get_account_info', views.get_account_info),
    path('get_my_invitation', views.get_my_invitation),
    path('gym_is_exist', views.gym_is_exist),
    path('login', views.login),
    path('store_info', views.store_info)
]
