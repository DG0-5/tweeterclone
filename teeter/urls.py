from django.urls import path
from .views import (
    home, profile_list, profile, logout_user, 
    login_user, register_user, update_user, 
    teep_like, teep_share, unfollow, follow, 
    followers, following, teep_delete, teep_edit,
    teep_search, search_user
)

urlpatterns = [
    path('', home, name='home'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile, name='profile'),
    path('profile/followers/<int:pk>', followers, name='followers'),
    path('profile/following/<int:pk>', following, name='following'),
    
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('update_user/', update_user, name='update_user'),
    path('teep_like/<int:pk>', teep_like, name='teep_like'),
    path('teep_share/<int:pk>', teep_share, name='teep_share'),
    path('unfollow/<int:pk>', unfollow, name='unfollow'),
    path('follow/<int:pk>', follow, name='follow'),
    path('teep_delete/<int:pk>', teep_delete, name='teep_delete'),
    path('teep_edit/<int:pk>', teep_edit, name='teep_edit'),
    path('search/', teep_search, name='search'),
    path('search_user/', search_user, name='search_user'),
]
