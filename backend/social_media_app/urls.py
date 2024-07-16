from django.urls import path
from . import views

#TODO add the rest of urls
urlpatterns = [
    path("send-friend-request", views.send_friend_request),
    path("accept-friend-request", views.accept_friend_request),
    path("decline-friend-request", views.decline_friend_request),
    path("remove-friend", views.remove_friend),
    path("get-all-friends", views.get_all_friends),
    path("get-friendship-status", views.get_friendship_status),
    path("get-friends-posts", views.get_friends_posts),
    path("get-user-posts", views.get_user_posts),
    path("get-user", views.get_user),
    path("get-friend-requests", views.get_friend_requests)
]
