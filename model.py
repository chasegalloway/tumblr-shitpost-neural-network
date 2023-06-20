import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import glob

# Step 1: Data Collection and Preprocessing
# Read data from multiple CSV files
file_pattern = 'TumblrPosts-1687204101-pukicho.csv'
csv_files = glob.glob(file_pattern)

posts = []
for file in csv_files:
    data = pd.read_csv(file)
    posts.extend(data['body'].tolist())

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

# Step 6: Generating Text
seed_text = "Your starting prompt"
next_words = 100

for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    predicted = np.argmax(model.predict(token_list), axis=-1)
    output_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    seed_text += " " + output_word

# Step 7: Saving the Generated Text
with open('generated_text.txt', 'w') as f:
    f.write(seed_text)
