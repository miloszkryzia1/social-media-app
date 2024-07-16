package com.learning.socialmediaapp.retrofit

import com.learning.socialmediaapp.retrofit.pojo.Account
import retrofit2.http.GET
import retrofit2.http.Query

interface SocialService {
    //TODO add calls
    /*
     * GET:
     * - get user info
     * - get all posts from a user
     * - get friends' posts
     * - get comments for post
     * - get likes
     * - get user's friends
     * - get friendship status between two users
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

    @GET("get-user")
    suspend fun getUserInfo(@Query("user_id") userId: Int): Account
}