import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
import pickle

model = load_model('tumblr_model.h5')

with open('tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

ngram_data = ['end of phrase', 'logical stop', 'conclusion', 'that was it']

seed_text = input("Enter a few words to start the post: ")

# Maximum number of words to generate
max_words = 20

# Generate the post
for _ in range(max_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=model.input_shape[1], padding='pre')
    predicted = np.argmax(model.predict(token_list), axis=-1)
    output_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    seed_text += " " + output_word

    # Check if the generated word indicates a logical end
    if any(ngram in seed_text for ngram in ngram_data):
        break

print("Generated Tumblr post:")
print(seed_text)
