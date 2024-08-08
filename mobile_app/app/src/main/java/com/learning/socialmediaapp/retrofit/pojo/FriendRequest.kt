package com.learning.socialmediaapp.retrofit.pojo

import com.google.gson.annotations.SerializedName

data class FriendRequest(
    @SerializedName("id")
    val id: Int,
    @SerializedName("from_user_id")
    val fromUserId: Int,
    @SerializedName("to_user_id")
    val toUserId: Int,
    @SerializedName("status")
    val status: String
) {
    override fun toString(): String {
        return "FriendRequest(id=$id, fromUserId=$fromUserId, toUserId=$toUserId, status='$status')"
    }
}


