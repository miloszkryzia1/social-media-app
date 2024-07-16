package com.learning.socialmediaapp.retrofit.pojo

import com.google.gson.annotations.SerializedName
import java.util.Date

data class Post(
    val id: Int,
    @SerializedName("author_id")
    val authorId: Int,
    val text: String,
    //TODO: add image
    val datetime: Date, //TODO make sure this is the right data type
    @SerializedName("likes")
    val likeCount: Int,
    @SerializedName("comments")
    val commentCount: Int
)
