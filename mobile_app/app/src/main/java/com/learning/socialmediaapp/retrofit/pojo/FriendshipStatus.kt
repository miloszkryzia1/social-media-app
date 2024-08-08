package com.learning.socialmediaapp.retrofit.pojo

import com.google.gson.annotations.SerializedName

data class FriendshipStatus(
    @SerializedName("status")
    val status: String
)
