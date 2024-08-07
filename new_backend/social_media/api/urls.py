from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.AccountListCreateView.as_view()),
    path("accounts/<int:pk>", views.AccountRetrieveUpdateDestroyView.as_view()),
    path("friendrequest/", views.FriendRequestListCreateView.as_view()),
    path("friendrequest/<int:pk>", views.FriendRequestRetrieveUpdateDestroyView.as_view()),
    path("friendship/", views.FriendshipRetrieveView.as_view()),
    path("posts/", views.PostListCreateView.as_view()),
    path("posts/<int:pk>", views.PostRetrieveUpdateDestroyView.as_view()),
    path("likes/", views.LikeListCreateView.as_view()),
    path("likes/<int:pk>", views.LikeDestroyView.as_view()),
    path("comments/", views.CommentListCreateView.as_view()),
    path("comments/<int:pk>", views.CommentRetrieveUpdateDestroyView.as_view())
]
