import os


class Config:
    HOST = '0.0.0.0'
    PORT = 8081


class ElasticSearchConfig:
    ELASTICSEARCH_IP_ADDRESS = 'localhost'
    ELASTICSEARCH_PORT = 9200
    INDEX_IMAGE = 'images'
