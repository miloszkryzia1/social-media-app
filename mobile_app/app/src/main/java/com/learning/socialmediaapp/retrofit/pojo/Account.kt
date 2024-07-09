package com.learning.socialmediaapp.retrofit.pojo

import com.google.gson.annotations.SerializedName
import java.util.Date

data class Account (
    @SerializedName("id")
    val id: Int,
    @SerializedName("first_name")
    val firstName: String,
    @SerializedName("last_name")
    val lastName: String,
    @SerializedName("email")
    val email: String,
    @SerializedName("date_of_birth")
    val dateOfBirth: Date
)

//TODO: add other pojos