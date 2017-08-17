package com.facemess;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;

/**
 * Created by Danish Shah on 13-08-2017.
 */

public class SplashActivity extends AppCompatActivity {

    Button login, signup;
    ProgressBar progressBar;

    Handler handler;

    boolean logged_in = false;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        handler = new Handler();

        login = (Button) findViewById(R.id.login);
        signup = (Button) findViewById(R.id.signup);

        progressBar = (ProgressBar) findViewById(R.id.splash_prog);

        if (logged_in){
            progressBar.setVisibility(View.VISIBLE);
            login.setVisibility(View.GONE);
            signup.setVisibility(View.GONE);

            // Check for user details and cache them.

            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    startActivity(new Intent(SplashActivity.this, MainActivity.class));
                    finish();
                }
            }, 1000);
        }else{
            progressBar.setVisibility(View.GONE);
            login.setVisibility(View.VISIBLE);
            signup.setVisibility(View.VISIBLE);
        }


        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Handle Login
                startActivity(new Intent(SplashActivity.this, MainActivity.class));
                finish();
            }
        });

        signup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Handle Sign Up
                startActivity(new Intent(SplashActivity.this, MainActivity.class));
                finish();
            }
        });
    }
}
