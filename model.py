import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Read data from a text file
text_file = 'TumblrPosts-1687218509-pukicho.txt'

with open(text_file, 'r', encoding='utf-8') as f:
    text_data = f.read()

# Preprocessing
posts = text_data.split('\n')

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

model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
model.add(LSTM(150))
model.add(Dense(total_words, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

history = model.fit(X, tf.keras.utils.to_categorical(y, num_classes=total_words),
                    epochs=50, verbose=1)

model.save('tumblr_model.h5')
