import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load FAQ data
data = pd.read_csv('data/faq_data.csv')

# Vectorize the questions
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['question'])

# Save the model and vectorizer
with open('chatbot_model.pkl', 'wb') as model_file:
    pickle.dump((vectorizer, X, data), model_file)

print("Model trained and saved successfully!")
