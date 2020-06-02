from elasticsearch import Elasticsearch, ConflictError, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl import A

from app.configuration.config import ElasticSearchConfig
import uuid

es = Elasticsearch(
    [{'host': ElasticSearchConfig.ELASTICSEARCH_IP_ADDRESS, 'port': ElasticSearchConfig.ELASTICSEARCH_PORT}])


def save_img(name, label, caption):
    img = {
        'name': name,
        'label': label,
        'caption': caption
    }
    try:
        res = es.index(index=ElasticSearchConfig.INDEX_IMAGE, id=uuid.uuid1(), body=img)
        print("image saved")
        return 1
    except:
        print("error")
        return 0


def get_image_by_id(id):
    try:
        res = es.get(index=ElasticSearchConfig.INDEX_IMAGE, id=id)
        return res['_source']
    except NotFoundError:
        print("imgage not found")


def get_image_by_name(name):
    query = {
        "query": {
            "match_phrase": {
                "name": name
            }
        }
    }
    try:
        res = es.search(index=ElasticSearchConfig.INDEX_IMAGE, body=query)
        return res['hits']['hits'][0]['_source']
    # if not found res will not contain ['hits']['hits'][0]['_source']
    except IndexError:
        print("images not found")


def get_image_by_label(label):
    query = {
        "query": {
            "match_phrase": {
                "label": label
            }
        }
    }
    try:
        res = es.search(index=ElasticSearchConfig.INDEX_IMAGE, body=query)
        imgs = []
        for i in res['hits']['hits']:
            imgs.append(i['_source'])
        return imgs
    # if not found res will not contain ['hits']['hits'][0]['_source']
    except IndexError:
        print("images not found")


def get_image():
    query = {
        "query": {
            "match_all": {}
        }
    }
    try:
        res = es.search(index=ElasticSearchConfig.INDEX_IMAGE, body=query)
        return res['hits']['hits']
    # if not found res will not contain ['hits']['hits'][0]['_source']
    except IndexError:
        print("have no image")


def get_label():
    try:
        imgs = get_image()
        labels = set()
        for img in imgs:
            labels.add(img['_source']['label'])

        return labels
    # if not found res will not contain ['hits']['hits'][0]['_source']
    except IndexError:
        print("have no image")


def fulltext_search(text):
    query = {
        "query": {
            "multi_match": {
                "query": text,
                "fields": ["label", "caption"]
            }
        }
    }
    try:
        res = es.search(index=ElasticSearchConfig.INDEX_IMAGE, body=query)
        imgs=[]
        for img in res['hits']['hits']:
            imgs.append(img["_source"])
        return imgs
    # if not found res will not contain ['hits']['hits'][0]['_source']
    except IndexError:
        print("have no image")


# print(fulltext_search('good'))
# es.indices.delete(index=ElasticSearchConfig.INDEX_IMAGE, ignore=[400, 404])
# example:

# for i in get_label():
#     print(i)
# print(get_image_by_name('100000.jpg'))
# print(get_image_by_label("general"))
