from . import models
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

"""
List of endpoints needed:

TODO: DESCRIBE ALL REQUIRED PARAMETERS / REQUEST TYPES FOR EACH ENDPOINT

Friends:
- send friend request - requires sending user id & receiving user id
- accept friend request - requires friend request id
- decline friend request
- remove friend
- get all friends of a user
- get all friend requests sent to a user
- get friendship status between 2 users (friends/notfriends/request sent)

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
"""
@csrf_exempt
def send_friend_request(request):
    from_user = models.Account.objects.get(id=request.POST["from_user_id"])
    to_user = models.Account.objects.get(id=request.POST["to_user_id"])
    fr = models.FriendRequest(from_user=from_user, to_user=to_user)
    fr.save()
    return HttpResponse("Friend request sent", status=200)

@csrf_exempt
def accept_friend_request(request):
    fr = models.FriendRequest.objects.get(id=request.POST["fr_id"])
    fr.to_user.friend.add(models.Account.objects.get(id=fr.from_user.id))
    fr.delete()
    return HttpResponse("Friend addded", status=200)

@csrf_exempt
def decline_friend_request(request):
    fr = models.FriendRequest.objects.get(id=request.POST["fr_id"])
    fr.status = "declined"
    fr.save()
    return HttpResponse("Friend request declined")

@csrf_exempt
def remove_friend(request):
    acc_1_id = request.POST["user_1_id"]
    acc_2_id = request.POST["user_2_id"]
    acc_1 = models.Account.objects.get(id=acc_1_id)
    acc_2 = models.Account.objects.get(id=acc_2_id)
    acc_1.friend.remove(acc_2)
    return HttpResponse("Friend removed", status=200)

def get_all_friends(request):
    user_id = request.GET["user_id"]
    user = models.Account.objects.get(id=user_id)
    friends_list = list(user.friend.all().values())
    return JsonResponse(friends_list, safe=False)

def get_friend_requests(request):
    to_user_id = request.GET["to_user_id"]
    frs = models.FriendRequest.objects.filter(to_user=models.Account.objects.get(id=to_user_id), status="sent")
    frs_list = list(frs.values())
    return JsonResponse(frs_list, safe=False)

def get_friendship_status(request):
    acc_1_id = request.GET['user_1_id']
    acc_2_id = request.GET['user_2_id']
    acc_1 = models.Account.objects.get(id=acc_1_id)
    acc_2 = models.Account.objects.get(id=acc_2_id)
    #friends / requested / request sent
    try: 
        #check if friends
        friend = acc_1.friend.get(id=acc_2_id)
        return HttpResponse("friends", status=200)
    except models.Account.DoesNotExist:
        #check if request sent or received
        fr_received = models.FriendRequest.objects.filter(to_user=acc_1, from_user=acc_2)
        fr_sent = models.FriendRequest.objects.filter(to_user=acc_2, from_user=acc_1)
        if len(fr_received.values()) > 0:
            return HttpResponse("fr_received", status=200)
        elif len(fr_sent.values()) > 0:
            return HttpResponse("fr_sent", status=200)
        return HttpResponse("not_friends", status=200)

#Posts

#TODO handle image in post
@csrf_exempt
def create_post(request):
    author_id = request.POST["user_id"]
    text = request.POST["text"]
    author = models.Account.objects.get(id=author_id)
    post = models.Post(author=author, text=text)
    post.save()
    return HttpResponse("Post created", status=200)

@csrf_exempt
def remove_post(request):
    post_id = request.POST["post_id"]
    post = models.Post.objects.get(id=post_id)
    post.delete()
    return HttpResponse("Post deleted", status=200)

@csrf_exempt
def edit_post(request):
    post_id = request.POST["post_id"]
    new_text = request.POST["new_text"]
    post = models.Post.objects.get(id=post_id)
    post.text = new_text
    post.save()
    return HttpResponse("Post edited", status=200)

@csrf_exempt
def comment_post(request):
    post_id = request.POST["post_id"]
    user_id = request.POST["user_id"]
    text = request.POST["text"]
    user = models.Account.objects.get(id=user_id)
    post = models.Post.objects.get(id=post_id)
    comment = models.Comment(user=user, post=post, text=text)
    comment.save()
    return HttpResponse("Comment created", status=200)

@csrf_exempt
def remove_comment(request):
    comment_id = request.POST["comment_id"]
    comment = models.Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponse("Comment deleted")

@csrf_exempt
def like_post(request):
    post_id = request.POST["post_id"]
    user_id = request.POST["user_id"]
    post = models.Post.objects.get(id=post_id)
    user = models.Account.objects.get(id=user_id)
    like = models.Like(user=user, post=post)
    like.save()
    return HttpResponse("Post liked")

@csrf_exempt
def remove_like(request):
    like_id = request.POST["like_id"]
    like = models.Like.objects.get(id=like_id)
    like.delete()
    return HttpResponse("Like removed")

def get_friends_posts(request):
    user_id = request.GET["user_id"]
    user = models.Account.objects.get(id=user_id)
    posts = []
    for f in user.friend.all():
        for p in f.post_set.all().values():
            posts.append(p)
    for p in posts:
        p["likes"] = models.Post.objects.get(id=p["id"]).like_count
        p["comments"] = models.Post.objects.get(id=p["id"]).comment_count
    return JsonResponse(posts, safe=False)

def get_user_posts(request):
    user_id = request.GET["user_id"]
    user = models.Account.objects.get(id=user_id)
    posts = list(user.post_set.all().values())
    for p in posts:
        p["likes"] = models.Post.objects.get(id=p["id"]).like_count
        p["comments"] = models.Post.objects.get(id=p["id"]).comment_count
    return JsonResponse(posts, safe=False)

#TODO add mroe endpoints as needed
#TODO document all functions

def get_user(request):
    user_id = request.GET["user_id"]
    user_data = models.Account.objects.filter(id=user_id).values()[0]
    user_data.pop("username")
    user_data.pop("password")
    return JsonResponse(user_data)

#TODO add login