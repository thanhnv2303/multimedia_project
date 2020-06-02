import glob

import numpy as np
from PIL import Image
from pickle import load
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from app.utils.model import CNNModel, generate_caption_beam_search
import os

from app.configuration.config import config

class ImageDescription:
    def __init__(self):
        assert type(
            config['max_length']) is int, 'Please provide an integer value for `max_length` parameter in config.py file'
        assert type(config[
                        'beam_search_k']) is int, 'Please provide an integer value for `beam_search_k` parameter in config.py file'
        self.tokenizer_path = config['tokenizer_path']
        self.tokenizer = load(open(self.tokenizer_path, 'rb'))

        # Max sequence length (from training)
        self.max_length = config['max_length']

        # Load the model
        self.caption_model = load_model(config['model_load_path'])

        self.image_model = CNNModel(config['model_type'])

    def extract_features(self,img, model, model_type):
        if model_type == 'inceptionv3':
            from keras.applications.inception_v3 import preprocess_input
            target_size = (299, 299)
        elif model_type == 'vgg16':
            from keras.applications.vgg16 import preprocess_input
            target_size = (224, 224)

        # Convert the image pixels to a numpy array
        image = img_to_array(img.resize(target_size))
        # Reshape data for the model
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        # Prepare the image for the CNN Model model
        image = preprocess_input(image)
        # Pass image into model to get encoded features
        features = model.predict(image, verbose=0)
        return features

    def descript(self,img):
        image = self.extract_features(img=img, model=self.image_model, model_type=config['model_type'])
        # Generate caption using Decoder RNN Model + BEAM search
        generated_caption = generate_caption_beam_search(self.caption_model, self.tokenizer, image, self.max_length,
                                                         beam_index=config['beam_search_k'])
        # Remove startseq and endseq
        caption = generated_caption.split()[1].capitalize()

        for x in generated_caption.split()[2:len(generated_caption.split()) - 1]:
            caption = caption + ' ' + x
        return caption

if __name__ == '__main__':
    img_des = ImageDescription()
    for img_path in sorted(glob.glob('../static/images/*.jpg')):
        print(img_path)
        img = Image.open(img_path)  # PIL image
        print(img_des.descript(img))
