# keras
from keras.models import Model
from keras.layers import Dense, Dropout
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet import MobileNet
from keras.applications.mobilenet import preprocess_input as mobilenet_preprocess_input
from keras.applications.nasnet import NASNetMobile, preprocess_input
from keras.applications.nasnet import preprocess_input as nasnet_preprocess_input
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input as inception_resnet_preprocess_input

# backend
import numpy as np

# NIMA util
from score_utils import mean_score, std_score

# etc
import argparse
import glob
from tqdm import tqdm

def get_argument_parser():
    parser = argparse.ArgumentParser(description='Evaluate NIMA(MobileNet, NasNet, InceptionResNet)')
    parser.add_argument('-img_dir', type=str, default=None, help='Pass a directory to evaluate the images in it(.png, .jpg, .jpeg)')
    parser.add_argument('-img_resize', type=str, default='false', help='Resize images to 224x224 before scoring')
    parser.add_argument('-network', type=str, default='MobileNet', help='The network to use.(MobileNet, NasNet, InceptionResNet)')
    parser.add_argument('-weight', type=str, default=None, help='Pass a trained weight path to evaluate the images in it')
    
    return parser

def parse_argument(args):
    ret = {}
    ret['img_dir'] = args.img_dir
    ret['img_resize'] = args.img_resize.lower() in ('true', 'yes', 't')
    ret['target_size'] = (224, 224) if ret['img_resize'] else None
    ret['network'] = args.network if args.network in ('MobileNet', 'NasNet', 'InceptionResNet') else None
    ret['weight'] = args.weight

    # Print configs
    print("test image dir    :", ret['img_dir'])
    print("image resize      :", ret['img_resize'])
    print("image target_size :", ret['target_size'])
    print("network           :", ret['network'])
    print("weight            :", ret['weight'])

    return ret

def get_image_list(image_dir):
    if image_dir is not None:
        print("Loading images from directory : ", image_dir)
        images = glob.glob(image_dir + '/*.png')
        images += glob.glob(image_dir + '/*.jpg')
        images += glob.glob(image_dir + '/*.jpeg')

    else:
        raise RuntimeError('Either -img_dir arguments must be passed as argument')

    return images

def set_model(network, weight):
    print("[Build model]")

    if network == 'MobileNet':
        print("Use MobileNet")
        base_model = MobileNet((None, None, 3), alpha=1, include_top=False, pooling='avg', weights=None)

    elif network == 'NasNet':
        print("Use NasNet")
        base_model = NASNetMobile((224, 224, 3), include_top=False, pooling='avg', weights=None)

    elif network == 'InceptionResNet':
        print("Use InceptionResNet")
        base_model = InceptionResNetV2(input_shape=(None, None, 3), include_top=False, pooling='avg', weights=None)

    else:
        raise RuntimeError('Either -network arguments must be passed as argument')
    
    x = Dropout(0.75)(base_model.output)
    x = Dense(10, activation='softmax')(x)
    model = Model(base_model.input, x)
    model.load_weights(weight)
    
    return model

def prediction_score(model, network, images, target_size):
    print("[Prediction score Images]")
    score_list = []

    for img_path in tqdm(images):
        #print("Evaluating : ", img_path)
        img = load_img(img_path, target_size=target_size)
        img = preprocess_img(img, network)
        scores = model.predict(img, batch_size=1, verbose=0)[0]
        score_list.append((img_path, mean_score(scores), std_score(scores)))
        #print("NIMA Score : %0.3f +- (%0.3f)" % (mean, std) + "\n")

    return score_list

def preprocess_img(img, network):
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0) 
    x = mobilenet_preprocess_input(x)
    
    if network == 'MobileNet':
        x = mobilenet_preprocess_input(x)

    elif network == 'NasNet':
        x = nasnet_preprocess_input(x)

    elif network == 'InceptionResNet':
        x = inception_resnet_preprocess_input(x)

    else:
        raise RuntimeError('Either -network arguments must be passed as argument')
    
    return x

def ranking_score(score_list):
    print("[Ranking Images]")
    rank_list = []
    score_list = sorted(score_list, key=lambda x: x[1], reverse=True)

    for i, (name, mean, std) in enumerate(score_list):
        print("[%3d]" % (i + 1), "%-35s : NIMA Score = %0.3f +- (%0.3f)" % (name, mean, std))
        rank_list.append((name, mean, std))

    return rank_list

import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.core.protobuf import saved_model_pb2
from tensorflow.python.util import compat


if __name__ == "__main__":
    parser = get_argument_parser()    
    config = parse_argument(parser.parse_args())
    
    images = get_image_list(config['img_dir'])
    print ("Number of testing examples : " + str(len(images)))
    
    model = set_model(config['network'], config['weight'])
    score_list = prediction_score(model, config['network'], images, config['target_size'])

    rank_list = ranking_score(score_list)

    parser = get_argument_parser()    
    config = parse_argument(parser.parse_args())
    model = set_model(config['network'], config['weight'])

    converter = tf.contrib.lite.TFLiteConverter.from_keras_model_file("test.h5")
    tflite_model = converter.convert()
    open("converted_model.tflite", "wb").write(tflite_model)
