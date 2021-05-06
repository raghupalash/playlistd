from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add/<str:type>', views.add, name="add"),
    path('add/<str:type>/<int:limit>', views.add, name="show_more"),
    path('edit', views.edit, name="edit"),
    path('edit/<str:id>', views.edit, name="edit_playlist"),
    path('your_taste', views.taste, name="your_taste"),
    path('sign_out', views.sign_out, name="sign_out")
]