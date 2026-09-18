from django.urls import path
from . import views


urlpatterns = [

    # HOME
    path(
        '',
        views.home,
        name='home'
    ),

    # AUTHENTICATION
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_user,
        name='login'
    ),

    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),

    # FEED
    path(
        'feed/',
        views.feed,
        name='feed'
    ),

    # CREATE POST
    path(
        'create-post/',
        views.create_post,
        name='create_post'
    ),

    # EDIT POST
    path(
        'edit-post/<int:post_id>/',
        views.edit_post,
        name='edit_post'
    ),

    # DELETE POST
    path(
        'delete-post/<int:post_id>/',
        views.delete_post,
        name='delete_post'
    ),

    # COMMENTS
    path(
        'comment/<int:post_id>/',
        views.add_comment,
        name='add_comment'
    ),

    # DELETE COMMENT
    path(
        'delete-comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment'
    ),

    # LIKE / UNLIKE
    path(
        'like/<int:post_id>/',
        views.toggle_like,
        name='toggle_like'
    ),

    # MY PROFILE
    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    # EDIT PROFILE
    path(
        'edit-profile/',
        views.edit_profile,
        name='edit_profile'
    ),

    # OTHER USER PROFILE
    path(
        'user/<str:username>/',
        views.user_profile,
        name='user_profile'
    ),

    # FOLLOW / UNFOLLOW
    path(
        'follow/<str:username>/',
        views.toggle_follow,
        name='toggle_follow'
    ),

    # SEARCH USERS
    path(
        'search/',
        views.search_users,
        name='search_users'
    ),
]