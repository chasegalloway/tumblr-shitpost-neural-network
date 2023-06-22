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

# Temperature parameter for text generation (higher values for more randomness, lower for more deterministic)
temperature = 0.01

# Generate the post
for _ in range(max_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=model.input_shape[1], padding='pre')
    predicted_probs = model.predict(token_list)[0]
    predicted_probs = predicted_probs / np.sum(predicted_probs)  # Normalize the probabilities
    predicted_probs = np.log(predicted_probs) / temperature
    exp_preds = np.exp(predicted_probs)
    predicted_probs = exp_preds / np.sum(exp_preds)
    predicted_id = np.random.choice(len(predicted_probs), p=predicted_probs)
    output_word = tokenizer.index_word[predicted_id]

    seed_text += " " + output_word

    # Check if the generated word indicates a logical end
    if any(ngram in seed_text for ngram in ngram_data):
        # Trim the generated post to the last complete sentence
        last_sentence = seed_text.rsplit('.', 1)[0] + '.'
        seed_text = last_sentence
        break

print("Generated Tumblr post:")
print(seed_text)
