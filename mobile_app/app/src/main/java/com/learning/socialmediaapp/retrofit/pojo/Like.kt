package com.learning.socialmediaapp.retrofit.pojo

import com.google.gson.annotations.SerializedName

data class Like(
    val id: Int,
    @SerializedName("user_id")
    val userId: Int,
    @SerializedName("post_id")
    val postId: Int
)
