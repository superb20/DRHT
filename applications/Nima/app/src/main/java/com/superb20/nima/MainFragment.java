package com.superb20.nima;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.superb20.nima.Common.PermissionHelper;

import java.io.IOException;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

/**
 * Created by Superb20 on 2019-02-14.
 */

public class MainFragment extends Fragment implements View.OnClickListener {
    private final static String TAG = "MainFragment";
    private final static String MODEL_PATH = "mobilenet_model.tflite";
    private final static int REQUEST_GALLERY = 0;
    private final static int IMAGE_RESIZE_WIDTH = 224;
    private final static int IMAGE_RESIZE_HEIGHT = 224;

    private NIMA mNima = null;
    private Executor mExecutor = Executors.newSingleThreadExecutor();

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(TAG, "onCreate()");

        try {
            initTensorFlowAndLoadModel();
        } catch (IOException e) {
            Log.e(TAG, "onCreate() fail");
            e.printStackTrace();
            getActivity().finish();
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
        view.findViewById(R.id.btn_album).setOnClickListener(this);
    }

    @Override
    public void onResume() {
        Log.i(TAG, "onResume()");
        super.onResume();

        if (!PermissionHelper.hasStoragePermission(getActivity())) {
            Log.d(TAG, "has not storage permission");
            PermissionHelper.requestStoragePermission(getActivity());
            return;
        }
    }

    @Override
    public void onDestroy() {
        Log.i(TAG, "onDestroy()");
        super.onDestroy();
        mExecutor.execute(new Runnable() {
            @Override
            public void run() {
                mNima.close();
            }
        });
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.btn_album:
                loadAlbum();
                break;
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode != Activity.RESULT_OK)
            return;

        if (requestCode == REQUEST_GALLERY) {
            Uri selectedImage = data.getData();

            try {
                Bitmap bitmap = MediaStore.Images.Media.getBitmap(getActivity().getContentResolver(), selectedImage);
                mNima.imageAssessment(bitmap);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void loadAlbum() {
        Intent i = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(i, REQUEST_GALLERY);
    }

    private void initTensorFlowAndLoadModel() throws IOException {
        mExecutor.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    mNima = NIMA.create(getActivity().getAssets(), MODEL_PATH, IMAGE_RESIZE_HEIGHT, IMAGE_RESIZE_WIDTH);
                } catch (final Exception e) {
                    throw new RuntimeException("Error initializing TensorFlow!", e);
                }
            }
        });
    }
}
