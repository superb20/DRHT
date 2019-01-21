# keras
from keras.applications.mobilenet import MobileNet
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet import preprocess_input

# backend
import numpy as np

# NIMA util
from score_utils import mean_score, std_score

# etc
import argparse
import glob

def get_image_list(image_dir):
    if image_dir is not None:
        print("Loading images from directory : ", image_dir)
        images = glob.glob(image_dir + '/*.png')
        images += glob.glob(image_dir + '/*.jpg')
        images += glob.glob(image_dir + '/*.jpeg')

    else:
        raise RuntimeError('Either -dir arguments must be passed as argument')

    return images

def get_score(scores):
    return mean_score(scores), std_score(scores)

def preprocess_img(img):
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def set_argument_parser():
    parser = argparse.ArgumentParser(description='Evaluate NIMA(MobileNet)')
    parser.add_argument('-dir', type=str, default=None, help='Pass a directory to evaluate the images in it')
    parser.add_argument('-resize', type=str, default='false', help='Resize images to 224x224 before scoring')
    parser.add_argument('-rank', type=str, default='true', help='Whether to tank the images after they have been scored')
    
    return parser

def parse_argument_parser(parser):
    args = parser.parse_args()
    resize_image = args.resize.lower() in ('true', 'yes', 't', '1')
    target_size = (224, 224) if resize_image else None
    rank_images = args.rank.lower() in ("true", "yes", "t", "1")
    image_dir = args.dir

    # Print configs
    print("image resize      :", resize_image)
    print("image target_size :", target_size)
    print("print ranking     :", rank_images)

    return resize_image, target_size, rank_images, image_dir

def set_model(weight):
    base_model = MobileNet((None, None, 3), alpha=1, include_top=False, pooling='avg', weights=None)
    x = Dropout(0.75)(base_model.output)
    x = Dense(10, activation='softmax')(x)
    model = Model(base_model.input, x)
    model.load_weights(weight)
    return model

def prediction_score(images, target_size):
    # prediction score
    score_list = []

    for img_path in images:
        print("Evaluating : ", img_path)
        img = load_img(img_path, target_size=target_size)
        img = preprocess_img(img)
        scores = model.predict(img, batch_size=1, verbose=0)[0]

        mean, std = get_score(scores)
        score_list.append((img_path, mean))
        print("NIMA Score : %0.3f +- (%0.3f)" % (mean, std) + "\n")

    return score_list

def ranking_score(score_list):
    print("[Ranking Images]")
    rank_list = []

    score_list = sorted(score_list, key=lambda x: x[1], reverse=True)

    for i, (name, score) in enumerate(score_list):
        print("[%3d]" % (i + 1), "%-35
        s : Score = %0.5f" % (name, score))
        rank_list.append((name, score))

if __name__== "__main__":
    parser = set_argument_parser()    
    resize_image, target_size, rank_images, image_dir = parse_argument_parser(parser)
    images = get_image_list(image_dir)
    model = set_model('weights/mobilenet_weights.h5')

    score_list = prediction_score(images, target_size)

    # rank images
    if rank_images:
        rank_list = ranking_score(score_list)
        
