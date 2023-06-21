import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import json
import pickle

# Step 1: Data Collection and Preprocessing
# Define a list of text files
text_files = ['TumblrPosts-1687218509-pukicho.txt', 'TumblrPosts-1687235429-biggest-gaudiest-patronuses.txt', 'TumblrPosts-1687235947-atsignchase.txt']

posts = []
for text_file in text_files:
    with open(text_file, 'r', encoding='utf-8') as f:
        text_data = f.read()
        posts.extend(text_data.split('\n'))

# Step 2: Tokenization and Sequence Generation
tokenizer = Tokenizer()
tokenizer.fit_on_texts(posts)
total_words = len(tokenizer.word_index) + 1

input_sequences = []
for post in posts:
    token_list = tokenizer.texts_to_sequences([post])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Pad sequences to ensure equal length
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

# Splitting into Input and Output
input_sequences = np.array(input_sequences)
X = input_sequences[:, :-1]
y = input_sequences[:, -1]

# Step 3: Neural Network Model
model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
model.add(LSTM(150))
model.add(Dense(total_words, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Step 4: Training the Model
history = model.fit(X, tf.keras.utils.to_categorical(y, num_classes=total_words),
                    epochs=50, verbose=1)

# Step 5: Saving the Model
model.save('tumblr_model.h5')

# Step 6: Saving the Tokenizer
tokenizer_data = tokenizer.to_json()
with open('tokenizer.json', 'w') as f:
    f.write(tokenizer_data)

# Step 7: Saving the Tokenizer using pickle
with open('tokenizer.pickle', 'wb') as f:
    pickle.dump(tokenizer, f)
