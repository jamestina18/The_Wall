from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('log-reg',views.log_reg),
    path('login',views.login),
    path('add-comment_wallmsg/<int:>',views.add_comment_wallmsg),
]