import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
import pickle

# Step 1: Load the trained model
model = load_model('tumblr_model.h5')

# Step 2: Load the tokenizer
with open('tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

# Step 3: Generate a Tumblr post
seed_text = input("Enter a few words to start the post: ")
next_words = 5

for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=model.input_shape[1], padding='pre')
    predicted = np.argmax(model.predict(token_list), axis=-1)
    output_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    seed_text += " " + output_word

print("Generated Tumblr post:")
print(seed_text)
