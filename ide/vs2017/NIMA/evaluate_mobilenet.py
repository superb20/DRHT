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

def get_image_list(args):
    # give priority to directory
    if args.dir is not None:
        print("Loading images from directory : ", args.dir)
        images = glob.glob(args.dir + '/*.png')
        images += glob.glob(args.dir + '/*.jpg')
        images += glob.glob(args.dir + '/*.jpeg')

    elif args.img[0] is not None:
        print("Loading images from path(s) : ", args.img)
        images = args.img

    else:
        raise RuntimeError('Either -dir or -img arguments must be passed as argument')

    return images

def get_score(scores):
    return mean_score(scores), std_score(scores)

def preprocess_img(img):
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

# Set argument parser
parser = argparse.ArgumentParser(description='Evaluate NIMA(MobileNet)')
parser.add_argument('-dir', type=str, default=None, help='Pass a directory to evaluate the images in it')
parser.add_argument('-img', type=str, default=[None], nargs='+', help='Pass one or more image paths to evaluate them')
parser.add_argument('-resize', type=str, default='false', help='Resize images to 224x224 before scoring')
parser.add_argument('-rank', type=str, default='true', help='Whether to tank the images after they have been scored')

# Parse arguments
args = parser.parse_args()
resize_image = args.resize.lower() in ('true', 'yes', 't', '1')
target_size = (224, 224) if resize_image else None
rank_images = args.rank.lower() in ("true", "yes", "t", "1")

# Print configs
print("image resize      :", resize_image)
print("image target_size :", target_size)
print("print ranking     :", rank_images)

images = get_image_list(args)

# Set model
base_model = MobileNet((None, None, 3), alpha=1, include_top=False, pooling='avg', weights=None)
x = Dropout(0.75)(base_model.output)
x = Dense(10, activation='softmax')(x)
model = Model(base_model.input, x)
model.load_weights('weights/mobilenet_weights.h5')

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

# rank images
if rank_images:
    print("[Ranking Images]")
    score_list = sorted(score_list, key=lambda x: x[1], reverse=True)

    for i, (name, score) in enumerate(score_list):
        print("[%3d]" % (i + 1), "%50s : Score = %0.5f" % (name, score))
