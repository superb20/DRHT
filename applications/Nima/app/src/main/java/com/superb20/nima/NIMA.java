package com.superb20.nima;

import android.content.res.AssetFileDescriptor;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.util.Log;

import org.tensorflow.lite.Interpreter;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;

/**
 * Created by Superb20 on 2019-02-28.
 */

public class NIMA {
    /**
     * Tag for the {@link Log}.
     */
    private static final String TAG = "NIMA";

    /**
     * An instance of the driver class to run model inference with Tensorflow Lite.
     */
    private Interpreter mInterpreter;

    static NIMA create(AssetManager assetManager, String modelPath) throws IOException {
        NIMA nima = new NIMA();
        nima.mInterpreter = new Interpreter(nima.loadModelFile(assetManager, modelPath), new Interpreter.Options());

        return nima;
    }

    // TensorFlowLite buffer with 602112 bytes and a ByteBuffer with 31610880 bytes.
    float imageAssessment(Bitmap bitmap) {
        Log.d(TAG, "imageAssessment()");
        ByteBuffer byteBuffer = convertBitmapToByteBuffer(bitmap);
        Log.d(TAG, "imageAssessment() 1");
        float[][] result = new float[1][10];
        Log.d(TAG, "imageAssessment() 2");
        mInterpreter.run(byteBuffer, result);
        Log.d(TAG, "imageAssessment() 3");

        for(int i = 0 ; i < 10; i++)
            Log.d(TAG, "result[" + i + "] : "  + result[0][i]);

        return 0.f;
    }

    private ByteBuffer convertBitmapToByteBuffer(Bitmap bitmap) {
        // Calculate how many bytes our image consists of.
        int bytes = 602112; // bitmap.getByteCount();
        ByteBuffer buffer = ByteBuffer.allocate(bytes); //Create a new buffer
        //bitmap.copyPixelsToBuffer(buffer); //Move the byte data to the buffer

        return buffer;
    }

    void close() {
        mInterpreter.close();
        mInterpreter = null;
    }

    /**
     * Memory-map the model file in Assets.
     */
    private MappedByteBuffer loadModelFile(AssetManager assetManager, String modelPath) throws IOException {
        AssetFileDescriptor fileDescriptor = assetManager.openFd(modelPath);
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        Log.d(TAG, "Created a Tensorflow Lite NIMA.");

        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }
}
