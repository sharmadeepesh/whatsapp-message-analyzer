from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('new_chat/',views.new_chat,name="new_chat"),
]
