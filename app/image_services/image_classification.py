import glob

from keras.applications import VGG19

from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
import numpy as np

# from keras import backend as K
#
# K.set_image_dim_ordering('tf')
import tensorflow as tf
from PIL import Image


class ImageClassificationVGG19:

    def __init__(self):
        self.graph = tf.compat.v1.get_default_graph
        self.inputShape = (224, 224)
        self.preprocess = imagenet_utils.preprocess_input
        self.model = VGG19(weights="imagenet")

    def predict(self, image):

        image1 = image.resize((224, 224))
        # image1 = image
        image1 = img_to_array(image1)

        image1 = np.expand_dims(image1, axis=0)

        # pre-process the image using the appropriate function based on the
        # model that has been loaded (i.e., mean subtraction, scaling, etc.)
        image1 = self.preprocess(image1)
        # classify the image
        preds = self.model.predict(image1)
        P = imagenet_utils.decode_predictions(preds)
        for (i, (imagenetID, label, prob)) in enumerate(P[0]):
            print("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))
        (imagenetID, label, prob) = P[0][0]
        if prob < 0.5:
            label = 'general'
        return label


# if __name__ == '__main__':
#     img_classification = ImageClassificationVGG19()
#     for img_path in sorted(glob.glob('../static/images/*.jpg')):
#         print(img_path)
#         img = Image.open(img_path)  # PIL image
#         print(img_classification.predict(img))
