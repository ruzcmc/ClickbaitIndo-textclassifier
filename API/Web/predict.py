import tensorflow as tf
import numpy as np
import pandas as pd

from transformers import BertTokenizer, TFBertModel
from tensorflow import keras
#from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# set maximum length and tokenizer
MAX_LEN = 22
tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-lite-base-p1')

# stopword
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

# load model on first launch
filename = "model/model.h5"
model = keras.models.load_model(filename)

def removeStopWords(sentence):
	sentence = stopword.remove(sentence)
	return sentence

def encodeText(sentence):
	sentence = removeStopWords(sentence)

	encoded_dict = tokenizer.encode_plus(
						sentence,
						add_special_tokens = True,
						max_length = MAX_LEN,
						pad_to_max_length = True,
						return_attention_mask = True,
						return_token_type_ids=False
	)

	input_ids = [encoded_dict['input_ids']]
	attn_mask = [encoded_dict['attention_mask']]
  	
	return input_ids, attn_mask

def predict(input):
	input_id, attn_mask = np.array(encodeText(input))
	data = [input_id, attn_mask]

	prediction = model.predict(data)
	prediction = (prediction > 0.5).astype("int32")
	prediction = prediction[0].item()

	return prediction