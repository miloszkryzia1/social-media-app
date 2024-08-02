from django.shortcuts import render
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.http import HttpResponse

"""
List of endpoints needed:

TODO: DESCRIBE ALL REQUIRED PARAMETERS / REQUEST TYPES FOR EACH ENDPOINT

Friends:
- send friend request - requires sending user id & receiving user id DONE
- accept friend request - requires friend request id DONE
- decline friend request DONE
- remove friend
- get all friends of a user
- get all friend requests sent to a user
- get friendship status between 2 users (friends/notfriends/request sent) DONE

Posts:
- create a post
- remove a post
- edit a post
- comment on a post
- remove comment
- like a post
- remove like
- get all friends posts
- get all posts from a user

GENERICS:
"""

#TODO handle username & password & account creation
# get users
class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

# add/post/delete users
class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = "pk"

#friend requests

#get/send friend requests
class FriendRequestListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    
    def get(self, request, *args, **kwargs):
        #get query params
        to_user_id = request.query_params.get("to_user", None)
        from_user_id = request.query_params.get("from_user", None)
        if to_user_id:
            user = Account.objects.get(id=to_user_id)
            queryset = FriendRequest.objects.filter(to_user=user)
        elif from_user_id:
            user = Account.objects.get(id=from_user_id)
            queryset = FriendRequest.objects.filter(from_user=user)
        else:
            return self.list(request, *args, **kwargs)

        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class FriendRequestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    lookup_field = "pk"

    #accept or change friend request status
    def patch(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        new_status = data["status"]
        if new_status == "accepted":
            acc_1 = Account.objects.get(id=instance.from_user.id)
            acc_2 = Account.objects.get(id=instance.to_user.id)
            acc_1.friend.add(acc_2)
            instance.delete()
            return Response("FR accepted and deleted", status=status.HTTP_204_NO_CONTENT)
        instance.status = new_status
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class FriendshipRetrieveView(generics.GenericAPIView):
    # provide users' ID's from request body
    # return user ids and status
    def get(self, request, *args, **kwargs):
        data = request.query_params
        user_id_1 = data.get("user_id_1", None)
        user_id_2 = data.get("user_id_2", None)
        acc_1 = Account.objects.get(id=user_id_1) #currently logged in on device sending request
        acc_2 = Account.objects.get(id=user_id_2)
        acc_1_friends = acc_1.friend
        response = {}
        try:
            #return friends
            acc_1_friends.get(id=acc_2.id)
            response["status"] = "friends"
        except Account.DoesNotExist:
            #return not friends, request sent, or request received
            try:
                fr = FriendRequest.objects.get(from_user=acc_1, to_user=acc_2)
                # if fr exists, check its status
                status = fr.status
                if status == "sent":
                    response["status"] = "frsent"
                elif status == "declined":
                    response["status"] = "notfriends"
            except FriendRequest.DoesNotExist:
                try:
                    fr = FriendRequest.objects.get(from_user=acc_2, to_user=acc_1)
                    status = fr.status
                    if status == "sent":
                        response["status"] = "frreceived"
                    elif status == "declined":
                        response["status"] = "notfriends"
                except FriendRequest.DoesNotExist:
                    response["status"] = "notfriends"
        return Response(response)