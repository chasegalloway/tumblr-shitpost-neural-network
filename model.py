import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import random

# Define a list of text files
text_files = ['TumblrPosts-biggest-gaudiest-patronuses.txt', 'TumblrPosts-firefox-official.txt', 'TumblrPosts-pukicho.txt']

posts = []
for text_file in text_files:
    with open(text_file, 'r', encoding='utf-8') as f:
        text_data = f.read()
        posts.extend(text_data.split('\n'))

# Specify the percentage of the dataset to use
percent_to_use = 0.8

# Shuffle the posts
random.shuffle(posts)

# Determine the number of posts to use based on the specified percentage
num_posts = int(len(posts) * percent_to_use)

# Select the desired portion of posts
selected_posts = posts[:num_posts]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(selected_posts)
total_words = len(tokenizer.word_index) + 1

input_sequences = []
for post in selected_posts:
    token_list = tokenizer.texts_to_sequences([post])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Pad sequences to ensure equal length
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

input_sequences = np.array(input_sequences)
X = input_sequences[:, :-1]
y = input_sequences[:, -1]

model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
model.add(LSTM(150, return_sequences=True))  # Add the first LSTM layer with return_sequences=True
model.add(Dropout(0.2))  # Add dropout after the first LSTM layer
model.add(LSTM(150))  # Add the second LSTM layer
model.add(Dense(total_words, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

history = model.fit(X, tf.keras.utils.to_categorical(y, num_classes=total_words),
                    epochs=50, verbose=1)

model.save('tumblr_model.h5')

tokenizer_data = tokenizer.to_json()
with open('tokenizer.json', 'w') as f:
    f.write(tokenizer_data)

with open('tokenizer.pickle', 'wb') as f:
    pickle.dump(tokenizer, f)
