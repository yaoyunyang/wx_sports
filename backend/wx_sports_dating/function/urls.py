from django.urls import path
from . import views

urlpatterns = [
    path('release', views.release_invitation),
    path('my_follows', views.get_my_follows),
    path('evaluate_gym', views.evaluate_gym),
    path('send_message', views.send_message)
]
