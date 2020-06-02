import os


class Config:
    HOST = '0.0.0.0'
    PORT = 8081


class ElasticSearchConfig:
    ELASTICSEARCH_IP_ADDRESS = 'localhost'
    ELASTICSEARCH_PORT = 9200
    INDEX_IMAGE = 'images'

# All paths are relative to train_val.py file

config = {
	'images_path': 'train_val_data/Flicker8k_Dataset/', #Make sure you put that last slash(/)
	'train_data_path': 'train_val_data/Flickr_8k.trainImages.txt',
	'val_data_path': 'train_val_data/Flickr_8k.devImages.txt',
	'captions_path': 'train_val_data/Flickr8k.token.txt',
	'tokenizer_path': 'app/model_data/tokenizer.pkl',
	'model_data_path': 'app/model_data/', #Make sure you put that last slash(/)
	'model_load_path': 'app/model_data/model_inceptionv3_epoch-20_train_loss-2.3519_val_loss-2.8424.hdf5',
	'num_of_epochs': 20,
	'max_length': 40, #This is set manually after training of model and required for test.py
	'batch_size': 64,
	'beam_search_k':3,
	'test_data_path': 'app/static/test_data/', #Make sure you put that last slash(/)
	'model_type': 'inceptionv3', # inceptionv3 or vgg16
	'random_seed': 1035
}

rnnConfig = {
	'embedding_size': 300,
	'LSTM_units': 256,
	'dense_units': 256,
	'dropout': 0.3
}
