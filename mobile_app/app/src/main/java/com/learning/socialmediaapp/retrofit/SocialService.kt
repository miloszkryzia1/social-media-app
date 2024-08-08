package com.learning.socialmediaapp.retrofit

import com.learning.socialmediaapp.retrofit.pojo.*
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.GET
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
     * - send friend request
     * - accept / decline friend request
     * - cancel friend request
     * - remove friend
     * - create post
     * - like
     * - comment
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
}