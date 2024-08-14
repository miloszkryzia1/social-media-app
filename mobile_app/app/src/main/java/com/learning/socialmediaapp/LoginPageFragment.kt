package com.learning.socialmediaapp

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.databinding.DataBindingUtil
import com.google.gson.Gson
import com.learning.socialmediaapp.databinding.FragmentLoginPageBinding
import com.learning.socialmediaapp.retrofit.MainRetrofit
import com.learning.socialmediaapp.retrofit.SocialService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.MediaType
import okhttp3.RequestBody

class LoginPageFragment : Fragment() {

    private var binding: FragmentLoginPageBinding? = null)

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        // Inflate the layout for this fragment
        binding = DataBindingUtil.inflate(inflater, R.layout.fragment_login_page, container, false)

        //TODO TESTING LOGIN

        val retrofit = MainRetrofit.getInstance()
        val service = retrofit.create(SocialService::class.java)
        binding!!.btnLogin.setOnClickListener {
            CoroutineScope(Dispatchers.IO).launch {
                val username = binding!!.edtUsername.text.toString()
                val password = binding!!.edtPassword.text.toString()
                val body = getRequestBody(username, password)
                //Log.i("LOGIN", body.toString())
                try {
                    val response = service.login(body)
                    Log.i("LOGIN", response.toString())
                } catch (e: retrofit2.HttpException) {
                    Log.e("LOGIN", "BODY ERROR")
                }
            }
        }
        return binding!!.root
    }

    private fun getRequestBody(username: String, password: String): RequestBody {
        val map = mapOf(
            "username" to username,
            "password" to password
        )
        val jsonData = Gson().toJson(map)
        Log.i("LOGIN", jsonData)
        val body = RequestBody.create(MediaType.get("application/json"), jsonData)
        return body
    }
}