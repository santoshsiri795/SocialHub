from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('upload_post',views.upload_post,name='upload_post'),
    path('comment/<str:pk>',views.comment,name='comment'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('edit_profile_pic',views.edit_profile_pic,name='edit_profile_pic'),
    path('edit_profile_thumb',views.edit_profile_thumb,name='edit_profile_thumb'),
    path('inbox',views.inbox,name='inbox'),
    path('like_post',views.like_post,name='like_post'),
    path('send_friend_request',views.send_friend_request,name='send_friend_request'),
    path('cancel_friend_request',views.cancel_friend_request,name='cancel_friend_request'),
    path('accept_friend_request',views.accept_friend_request,name='accept_friend_request'),
    path('decline_friend_request',views.decline_friend_request,name='decline_friend_request'),
    path('un_friend',views.un_friend,name='un_friend'),
    path('request_list',views.request_list,name='request_list'),
 

    
]