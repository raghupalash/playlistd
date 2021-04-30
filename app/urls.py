from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add', views.add, name="add"),
    path('sign_out', views.sign_out, name="sign_out")
]