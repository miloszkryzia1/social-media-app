from django.db import models

class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    date_of_birth = models.DateField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    friend = models.ManyToManyField("self", db_table="friendship")

    class Meta:
        db_table = "account"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="request_to_set")
    status = models.CharField(max_length=20, default="sent")

    class Meta:
        db_table = "friend_request"

class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    text = models.CharField(max_length=1000)
    image = models.ImageField()

    class Meta:
        db_table = "post"

class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = "like"

class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    class Meta:
        db_table = "comment"
