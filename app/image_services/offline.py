import glob
import os
import pickle
from PIL import Image

from app.image_services.feature_extractor import FeatureExtractorVGG16

# fe = FeatureExtractorVGG16()
#
# for img_path in sorted(glob.glob('../static/images/*.jpg')):
#     print(img_path)
#     img = Image.open(img_path)  # PIL image
#     feature = fe.extract(img)
#     print(feature)
#     feature_path = '../static/features/VGG16/' + os.path.splitext(os.path.basename(img_path))[0] + '.pkl'
#     pickle.dump(feature, open(feature_path, 'wb'))

# img_path = 'app/static/images/100000.jpg'
# img = Image.open('../static/images/100000.jpg')
# fe = FeatureExtractorVGG16()
# feature = fe.extract(img)
# feature_path = '../static/features/VGG16/' + os.path.splitext(os.path.basename(img_path))[0] + '.pkl'
# pickle.dump(feature, open(feature_path, 'wb'))

