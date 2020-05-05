import glob
import os
import pickle
import numpy as np
from PIL import Image

from app.image_services.feature_extractor import FeatureExtractorVGG16


class ImageSearchVGG16:
    def __init__(self, feature_extractor):
        self.fe = feature_extractor
        self.features = []
        self.img_paths = []
        for feature_path in glob.glob("app/static/features/VGG16/*"):
            self.features.append(pickle.load(open(feature_path, 'rb')))
            self.img_paths.append('/static_img/images/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')

    def search(self, img):
        if self.features:
            query = self.fe.extract(img)
            dists = np.linalg.norm(self.features - query, axis=1)  # Do search
            ids = np.argsort(dists)[:30]  # Top 30 results
            scores = [(dists[id], self.img_paths[id]) for id in ids]
            return scores
        else:
            return []
