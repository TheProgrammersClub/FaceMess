package com.facemess;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class SignupActivity extends AppCompatActivity {

    EditText nameInput;
    EditText emailInput;
    EditText passwordInput;
    EditText confirmPassword;

    String name, email, password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        nameInput = (EditText) findViewById(R.id.nameInput);
        emailInput = (EditText) findViewById(R.id.emailInput);
        passwordInput = (EditText) findViewById(R.id.passwordInput);
        confirmPassword = (EditText) findViewById(R.id.confirmPasswordInput);

    }

    public void signup(View view){

        name = nameInput.getText().toString();
        email = emailInput.getText().toString();
        password = passwordInput.getText().toString();
        if (password.equals(confirmPassword.getText().toString())){

        }
        else {

        }

    }

    public void googleSignup(View view){

    }

    public void facebookSignup(View view){

    }

}
