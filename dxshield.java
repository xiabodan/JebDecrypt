package com.example.myapplication;

public class dxshield {
    public static String E(String arg4) {
        int v0 = arg4.length();
        char[] v1 = new char[v0];
        --v0;
        while(v0 >= 0) {
            int v3 = v0 - 1;
            v1[v0] = ((char)(arg4.charAt(v0) ^ 50));
            if(v3 < 0) {
                break;
            }

            v0 = v3 - 1;
            v1[v3] = ((char)(arg4.charAt(v3) ^ 56));
        }
        String print = new String(v1);
        System.out.println("" + print);
        return new String(v1);
    }
}
