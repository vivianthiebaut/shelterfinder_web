from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.index),
    path("login/", views.user_login),
    path("register", views.user_register),
    path("",include("django.contrib.auth.urls")),
    path("home/", views.home),
    path("shelter/<int:id>", views.shelter_details),
]