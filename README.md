# NIMA: Neural Image Assessment

This is a Keras implementation of the paper [NIMA: Neural Image Assessment](https://arxiv.org/pdf/1709.05424.pdf) by Hossein Talebi and Peyman Milanfar.

Below is my mild stone.
1. Check other open source
2. Make full pipeline code.
3. Refactoring
4. Make some applications for performance test.

# Implementation Details
+ The model was trained on the [AVA: A Large-Scale Database for Aesthetic Visual Analysis](http://refbase.cvc.uab.es/files/MMP2012a.pdf), which contains roughly 255,500 images. You can get it from [here](https://github.com/mtobeiyf/ava_downloader).

# Usage
## Evaluation

python evaluate_mobilenet.py -dir test_images

python evaluate_nasnet.py -dir test_images -resize true


# References
1. Talebi, Hossein, and Peyman Milanfar. "NIMA: Neural Image Assessment." IEEE Transactions on Image Processing (2018).
2. [Introducing NIMA: Neural Image Assessment](https://ai.googleblog.com/2017/12/introducing-nima-neural-image-assessment.html) - Googla AI Blog

