import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import os
import re

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'dataset.csv')
model_path = os.path.join(current_dir, 'recruitment_model.pkl')

print("Loading dataset...")
try:
    data = pd.read_csv(csv_path)

    # Clean Data
    if 'Resume_str' in data.columns:
        data = data.rename(columns={'Resume_str': 'text'})
    elif 'Resume' in data.columns:
        data = data.rename(columns={'Resume': 'text'})
    else:
        data = data.rename(columns={data.columns[1]: 'text'})

    data = data.dropna(subset=['text'])

    print(f"Training on {len(data)} resumes...")

    # --- KEY CHANGE: INCREASE VOCABULARY ---
    # max_features=10000 ensures it learns rarer words like 'photographer'
    # min_df=1 means "learn a word even if it only appears ONCE"
    tfidf = TfidfVectorizer(stop_words='english', max_features=15000, min_df=1)

    tfidf_matrix = tfidf.fit_transform(data['text'])

    # We use NearestNeighbors for the model structure, but mainly we need the Vectorizer
    model = NearestNeighbors(n_neighbors=1, metric='cosine')
    model.fit(tfidf_matrix)

    # Save
    with open(model_path, 'wb') as f:
        pickle.dump((tfidf, model), f)

    print("Success! Model trained and saved to recruitment_model.pkl")

except Exception as e:
    print(f"Error: {e}")