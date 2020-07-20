package com.example.lazy;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        System.out.println("Hello World!");
        ConnectionThread connectionThread = new ConnectionThread();
        connectionThread.run();
    }
}
