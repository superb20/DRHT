# NIMA: Neural Image Assessment

This is a Keras implementation of the paper [NIMA: Neural Image Assessment](https://arxiv.org/pdf/1709.05424.pdf) by Hossein Talebi and Peyman Milanfar.




Quantification of image quality and aesthetics has been.

Below is my mild stone.
1. Check other open source. (Done)
2. Make estimate code. (Done)
3. Convert for Android version for performance test. #TODO
4. Make some application. #TODO
5. Make train code. #TODO
6. Refactoring and optimize. #TODO

# Implementation Details
+ The model was trained on the [AVA: A Large-Scale Database for Aesthetic Visual Analysis](http://refbase.cvc.uab.es/files/MMP2012a.pdf) by Naila Murray and Luca Marchesotti, which contains roughly 255,500 images. You can get it from [here](https://github.com/mtobeiyf/ava_downloader).
+ [TID2013](http://www.ponomarenko.info/tid2013.htm) used for technical ratings.

# Pretrained model
You can get it from [here](https://github.com/titu1994/neural-image-assessment/releases).

# Usage
## Evaluation
+ python evaluate_NIMA.py -img_dir test_images -img_resize true -network MobileNet -weight weights/mobilenet_weights.h5
+ python evaluate_NIMA.py -img_dir test_images -img_resize true -network NasNet -weight weights/nasnet_weights.h5
+ python evaluate_NIMA.py -img_dir test_images -img_resize true -network InceptionResNet -weight weights/inception_resnet_weights.h5

# Example Results


# References
1. Talebi, Hossein, and Peyman Milanfar. "NIMA: Neural Image Assessment." IEEE Transactions on Image Processing (2018).
2. "AVA: A Large-Scale Database for Aesthetic Visual Analysis." 
3. [Introducing NIMA: Neural Image Assessment](https://ai.googleblog.com/2017/12/introducing-nima-neural-image-assessment.html) - Googla AI Blog

