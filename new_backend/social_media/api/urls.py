from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.AccountListCreateView.as_view()),
    path("accounts/<int:pk>", views.AccountRetrieveUpdateDestroyView.as_view()),
    path("friendrequests/", views.FriendRequestListCreateView.as_view()),
    path("friendrequests/<int:pk>", views.FriendRequestRetrieveUpdateDestroyView.as_view())
]
