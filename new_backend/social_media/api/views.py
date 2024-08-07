from django.shortcuts import render
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.http import HttpResponse
from django.db.models import Q

"""

TODO: DOCUMENT EVERYTHING and CLEAN UP

"""

#TODO handle username & password & account creation

"""
GET /accounts/
opt params: friends_with_id - return only users that are friends of specified account

POST /accounts/
pass entire user data as body
"""
class AccountListCreateView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        friend_id = request.query_params.get("friends_with_id", None)
        if friend_id == None:        
            return self.list(request, *args, **kwargs)
        else:
            friend = Account.objects.get(id=friend_id)
            queryset = friend.friends.all()
            serializer = AccountSerializer(queryset, many=True)
            return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        data = request.data
        new_account = Account(first_name=data["first_name"], last_name=data["last_name"], email=data["email"], date_of_birth=data["date_of_birth"], username=data["username"], password=data["password"])
        new_account.save()
        serializer = AccountSerializerUserPassowrd(data)
        return Response(serializer.data)

# add/post/delete users
"""
GET, PUT, DELETE /accounts/id
"""
class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = "pk"

#friend requests

#get/send friend requests
"""
GET /friendrequests/
opt params: to_user, from_user - return with specfied filters

POST /friendrequests/
"""
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


"""
GET, PUT, DELETE /friendrequests/id

PATCH /friendrequests/id with body status=***accepted/rejected/canceled***
use to accept/deny/cancel FRs
"""
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
            acc_1.friends.add(acc_2)
            instance.delete()
            return Response("FR accepted and deleted", status=status.HTTP_204_NO_CONTENT)
        elif new_status == "canceled":
            instance.delete()
            return Response("FR deleted", status=status.HTTP_204_NO_CONTENT)
        instance.status = new_status
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
"""
GET /friendship/
with params user_id_1 and user_id_2
returns friendship status between two users

DELETE /friendship/ with body user_id_1 and user_id_2
removes friendship between two users
"""
class FriendshipRetrieveView(generics.GenericAPIView):

    # provide users' ID's from request body
    # return user ids and status
    def get(self, request, *args, **kwargs):
        data = request.query_params
        user_id_1 = data.get("user_id_1", None)
        user_id_2 = data.get("user_id_2", None)
        acc_1 = Account.objects.get(id=user_id_1) #currently logged in on device sending request
        acc_2 = Account.objects.get(id=user_id_2)
        acc_1_friends = acc_1.friends
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
    
    def delete(self, request, *args, **kwargs):
        data = request.query_params
        user_id_1 = data.get("user_id_1", None)
        user_id_2 = data.get("user_id_2", None)
        acc_1 = Account.objects.get(id=user_id_1) #currently logged in on device sending request
        acc_2 = Account.objects.get(id=user_id_2)
        acc_1_friends = acc_1.friends
        acc_1_friends.remove(acc_2)
        return Response("Friendship deleted", status=status.HTTP_200_OK)

"""
GET /posts/ 
opt params: author_id, friends_with_id 
get either all posts, posts by specified user, or posts by friends of specified user
"""
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        author_id = request.query_params.get("author_id", None)
        friends_with_id = request.query_params.get("friends_with_id", None)
        if author_id:
            queryset = Post.objects.filter(author=Account.objects.get(id=author_id))
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        elif friends_with_id:
            friends = Account.objects.get(id=friends_with_id).friends.all()
            queryset = Post.objects.filter(Q(author__in=friends))
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return self.list(request, *args, **kwargs)
        
"""
GET, PUT, DELETE /posts/id
"""
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "pk"

"""
GET /likes/
opt param post_id - get all likes under specified post
"""
class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        post_id = request.query_params.get("post_id", None)
        if post_id:
            queryset = Post.objects.get(id=post_id).like_set.all()
            serializer = LikeSerializer(queryset, many=True)
            return Response(serializer.data)
        return self.list(request, *args, **kwargs)
    
# unlike - maybe change to something more complex if needed, for now unlike by like id
"""
DELETE /likes/id
"""
class LikeDestroyView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "pk"

"""
GET /comments/
opt param post_id - get all comments under specified post
"""
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        post_id = request.query_params.get("post_id", None)
        if post_id:
            queryset = Post.objects.get(id=post_id).comment_set.all()
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)
        return self.list(request, *args, **kwargs)
    
"""
GET, PUT, DELETE /comments/id
"""
class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"