package com.example.lazy;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ConnectionThread extends Thread {
    @Override
    public void run() {
        super.run();
        try {
            Socket socket = new Socket("archie", 1234);
            BufferedReader sockInput = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter sockOutput = new PrintWriter(socket.getOutputStream(), true);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
