package com.learning.socialmediaapp.retrofit.pojo

import com.google.gson.annotations.SerializedName

data class Comment(
    val id: Int,
    @SerializedName("user_Id")
    val userId: Int,
    @SerializedName("post_id")
    val postId: Int,
    val text: String
) {
    override fun toString(): String {
        return "Comment(id=$id, userId=$userId, postId=$postId, text='$text')"
    }
}

