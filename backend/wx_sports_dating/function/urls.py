from django.urls import path
from . import views

urlpatterns = [
    path('release', views.release_invitation)
]