package com.learning.socialmediaapp

import android.os.Bundle
import android.util.Log
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.databinding.DataBindingUtil
import com.learning.socialmediaapp.databinding.ActivityMainBinding
import com.learning.socialmediaapp.retrofit.MainRetrofit
import com.learning.socialmediaapp.retrofit.SocialService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    private var binding: ActivityMainBinding? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = DataBindingUtil.setContentView(this, R.layout.activity_main)

        //TODO: add tests
        val retrofit = MainRetrofit.getInstance()
        val service = retrofit.create(SocialService::class.java)

        binding!!.button.setOnClickListener {
            CoroutineScope(Dispatchers.IO).launch {
                val responseObject = service.getUserInfo(1)
                Log.i("TEST", responseObject.toString())
            }
        }
        //get user info
    }


}