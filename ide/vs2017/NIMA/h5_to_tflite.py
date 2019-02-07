import tensorflow as tf

if __name__ == "__main__":
    converter = tf.contrib.lite.TocoConverter.from_keras_model_file('weights/mobilenet_model.h5')
    tflite_model = converter.convert()  
    open("converted_model.tflite", "wb").write(tflite_model)