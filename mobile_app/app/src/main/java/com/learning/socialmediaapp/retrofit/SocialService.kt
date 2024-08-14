package com.learning.socialmediaapp.retrofit

import com.learning.socialmediaapp.retrofit.pojo.*
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface SocialService {
    //TODO add calls
    /*
     * GET:
     * - get user info DONE
     * - get all posts from a user DONE
     * - get friends' posts DONE
     * - get comments for post DONE
     * - get likes DONE
     * - get user's friends DONE
     * - get friendship status between two users DONE
     * -
     *
     * POST:
     * - send friend request DONE
     * - accept / decline friend request DONE
     * - cancel friend request DONE
     * - remove friend DONE
     * - create post DONE
     * - like DONE
     * - comment DONE
     */

    @GET("accounts/")
    suspend fun getAllUsers(): List<Account>

    @GET("accounts/{userId}")
    suspend fun getUserInfo(@Path("userId") userId: Int): Account

    @GET("accounts/")
    suspend fun getFriends(@Query("friends_with_id") userId: Int): List<Account>

    //TODO idk if string works as return type, might need to make another class for the response
    @GET("friendship/")
    suspend fun getFriendshipStatus(
        @Query("user_id_1") userId1: Int,
        @Query("user_id_2") userId2: Int
    ): FriendshipStatus

    @GET("posts/")
    suspend fun getUserPosts(@Query("author_id") userId: Int): List<Post>

    @GET("posts/")
    suspend fun getFriendsPosts(@Query("friends_with_id") userId: Int): List<Post>

    @GET("comments/")
    suspend fun getComments(@Query("post_id") postId: Int): List<Comment>

    @GET("likes/")
    suspend fun getLikes(@Query("post_id") postId: Int): List<Like>

    @POST("friendrequests/")
    suspend fun sendFriendRequest(@Body friendRequest: FriendRequest)

    //request body is status=accepted/rejected/canceled
    @PATCH("friendrequests/{frId}")
    suspend fun processFriendRequest(
        @Path("frId") friendRequestId: Int,
        @Body requestBody: RequestBody
    ): ResponseBody

    @DELETE("friendship/")
    suspend fun removeFriend(
        @Query("user_id_1") userId1: Int,
        @Query("user_id_2") userId2: Int
    ): ResponseBody

    @POST("posts/")
    suspend fun createPost(@Body post: Post): Post

    @POST("likes/")
    suspend fun likePost(@Body like: Like): Like

    @POST("comments/")
    suspend fun commentPost(@Body comment: Comment): Comment
}