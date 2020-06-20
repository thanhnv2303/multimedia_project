from elasticsearch import Elasticsearch
from app.configuration.config import Config, ElasticSearchConfig

elastic_search = Elasticsearch(
    [{'host': ElasticSearchConfig.ELASTICSEARCH_IP_ADDRESS, 'port': ElasticSearchConfig.ELASTICSEARCH_PORT}])
if not elastic_search.indices.exists(index=ElasticSearchConfig.INDEX_IMAGE):
    elastic_search.indices.create(index=ElasticSearchConfig.INDEX_IMAGE)

from flask import Flask
from app.controller.index import index_api

app = Flask(__name__)

app.register_blueprint(index_api, static_folder=None)

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, threaded=False)
