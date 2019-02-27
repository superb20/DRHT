package com.superb20.nima;

import android.app.Activity;
import android.content.res.AssetFileDescriptor;
import android.util.Log;

import org.tensorflow.lite.Interpreter;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;

/**
 * Created by Superb20 on 2019-02-28.
 */

public class NIMA {
    /** Tag for the {@link Log}. */
    private static final String TAG = "NIMA";

    /** The loaded TensorFlow Lite model. */
    private MappedByteBuffer tfliteModel;

    /** An instance of the driver class to run model inference with Tensorflow Lite. */
    protected Interpreter tflite;

    /** Options for configuring the Interpreter. */
    private final Interpreter.Options tfliteOptions = new Interpreter.Options();

    NIMA(Activity activity) throws IOException {
        tfliteModel = loadModelFile(activity);
        tflite = new Interpreter(tfliteModel, tfliteOptions);

//        labelList = loadLabelList(activity);
//        imgData =
//                ByteBuffer.allocateDirect(
//                        DIM_BATCH_SIZE
//                                * getImageSizeX()
//                                * getImageSizeY()
//                                * DIM_PIXEL_SIZE
//                                * getNumBytesPerChannel());
//        imgData.order(ByteOrder.nativeOrder());
//        filterLabelProbArray = new float[FILTER_STAGES][getNumLabels()];
        Log.d(TAG, "Created a Tensorflow Lite NIMA.");
    }

    /**
     * Memory-map the model file in Assets.
     */
    private MappedByteBuffer loadModelFile(Activity activity) throws IOException {
        AssetFileDescriptor fileDescriptor = activity.getAssets().openFd(getModelPath());
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();

        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }

    /**
     * Get the name of the model file stored in Assets.
     *
     * @return
     */
    private String getModelPath() {
        return "mobilenet_model.tflite";
    }
}
