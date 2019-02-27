package com.superb20.nima;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.io.IOException;

/**
 * Created by Superb20 on 2019-02-14.
 */

// https://codelabs.developers.google.com/codelabs/tensorflow-for-poets-2-tflite/#3

public class MainFragment extends Fragment {
    private final static String TAG = "MainFragment";

    private NIMA mNima = null;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(TAG, "onCreate()");

        try {
            mNima = new NIMA(getActivity());
        } catch (IOException e) {
            Log.i(TAG, "onCreate() fail");
            e.printStackTrace();
        }
    }

    /**
     * Layout the preview and buttons.
     */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup parent, Bundle savedInstanceState) {
        Log.i(TAG, "onCreateView()");
        return inflater.inflate(R.layout.fragment_main, parent, false);
    }

    /**
     * Connect the buttons to their event handler.
     */
    @Override
    public void onViewCreated(final View view, Bundle savedInstanceState) {
        Log.i(TAG, "onViewCreated()");
    }

    /**
     * Load the model and labels.
     */
    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        Log.i(TAG, "onActivityCreated()");
    }
}
