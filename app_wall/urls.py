from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('log-reg',views.log_reg),
    path('log-in',views.log_in),
    path('logged',views.logged),
    path('add-post', views.add_post),
    path('wall_feed', views.wall_feed),
    path('logout',views.logout),
    path('edit/<int:id>', views.edit_post),
    path('edited-post',views.edited_post),
    path('add-comment',views.add_comment),
    # path('add-comment_wallmsg/<int:>',views.add_comment_wallmsg),
]