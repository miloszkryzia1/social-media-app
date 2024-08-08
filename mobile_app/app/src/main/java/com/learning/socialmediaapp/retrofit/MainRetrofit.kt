package com.learning.socialmediaapp.retrofit

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MainRetrofit {

    companion object {
        @Volatile
        var INSTANCE: Retrofit? = null
        private val LOCK = Any()
        private const val BASEURL = "http://10.0.2.2:8000/"

        fun getInstance(): Retrofit {
            return INSTANCE ?:
                synchronized(LOCK) {
                    val instance = Retrofit.Builder()
                        .baseUrl(BASEURL)
                        .addConverterFactory(GsonConverterFactory.create())
                        .build()

                    INSTANCE = instance
                    instance
                }
        }
    }

}