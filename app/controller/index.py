import glob
import os
import pickle

from PIL import Image
from flask import Blueprint, request, render_template,url_for, redirect

from app.image_services.feature_extractor import FeatureExtractorVGG16
from app.image_services.image_classification import ImageClassificationVGG19
from app.image_services.image_description import ImageDescription
from app.image_services.image_search import ImageSearchVGG16

from app.database_services.image_db import *

index_api = Blueprint('index_api', __name__,
                      template_folder='../templates',
                      static_folder='../static',
                      static_url_path='/static_img'
                      )
fe = FeatureExtractorVGG16()
img_classification = ImageClassificationVGG19()
img_description = ImageDescription()


@index_api.route("/", methods=['GET', 'POST'])
def home():
    images = []
    imgs = get_image()
    for img in imgs:
        img_path = '/static_img/images/' + img['_source']['name']
        caption = img['_source']['caption']
        images.append((img_path, caption))

    return render_template('home.html', images=images)


@index_api.route("/album", methods=['GET', 'POST'])
def album():
    if request.method == 'POST':
        label = request.form['label']
        imgs = get_image_by_label(label)
        for img in imgs:
            img['name'] = '/static_img/images/' + img['name']

        return render_template('album.html', labels=get_label(), label=label, images=imgs)
    else:
        return render_template('album.html', labels=get_label())


@index_api.route("/upload", methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        file = request.files['query_img']
        filename = file.filename
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "app/static/images/" + filename
        img.save(uploaded_img_path)

        label = img_classification.predict(img)

        description = img_description.descript(img)

        print(label)
        print(description)

        save_img(filename, label, description)

        feature = fe.extract(img)
        img_path = 'app/static/images/' + filename
        feature_path = 'app/static/features/VGG16/' + os.path.splitext(os.path.basename(img_path))[0] + '.pkl'
        pickle.dump(feature, open(feature_path, 'wb'))
        upload_path = "/static_img/images/" + filename
        return render_template('upload.html', upload_path=upload_path)
    else:
        return render_template('upload.html')


@index_api.route("/search/byImage", methods=['GET', 'POST'])
def search_by_img():
    if request.method == 'POST':
        file = request.files['query_img']
        filename = file.filename
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "app/static/uploaded/" + filename
        img.save(uploaded_img_path)
        img_upload = "/static_img/uploaded/" + filename

        print(img_upload)
        img_serach = ImageSearchVGG16(fe)
        scores = img_serach.search(img)
        return render_template('search.html',
                               img_upload=img_upload,
                               scores=scores)
    else:
        return render_template('search.html')


@index_api.route("/search/byText", methods=['GET', 'POST'])
def search_by_text():
    if request.method == 'POST':
        text = request.form['query_text']

        imgs = fulltext_search(text)
        for img in imgs:
            img['name'] = '/static_img/images/' + img['name']
        return render_template('search_text.html',
                               images=imgs)
    else:
        return render_template('search_text.html')
