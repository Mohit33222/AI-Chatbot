import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

# Download stopwords
nltk.download('stopwords')

FAQ_FILE = 'data/faq_data.csv'

def preprocess(text):
    """Preprocessing the text by lowercasing, removing stopwords, and stemming"""
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    # Lowercase and remove punctuation
    text = text.lower().translate(str.maketrans('', '', string.punctuation))

    # Tokenize and stem words
    tokens = text.split()
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]

    return ' '.join(tokens)

def get_response(user_input):
    try:
        data = pd.read_csv(FAQ_FILE)
        questions = data['question'].apply(preprocess).tolist()
        answers = data['answer'].tolist()

        if not questions:
            return "No FAQs available."

        # Preprocess the input
        user_input = preprocess(user_input)

        # Vectorizing the input and FAQ questions
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(questions + [user_input])
        similarity = cosine_similarity(vectors[-1], vectors[:-1])

        # Find the most similar FAQ
        max_similarity_index = similarity.argmax()
        if similarity[0, max_similarity_index] >= 0.5:   # Increased threshold
            return answers[max_similarity_index]
        else:
            return "I'm not sure. Please contact the administration."

    except Exception as e:
        return f"Error: {str(e)}"
