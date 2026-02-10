import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import os

# 1. Load the Data
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'dataset.csv')

print("Loading dataset...")
try:
    data = pd.read_csv(csv_path)

    # Clean up column names (just like in train_model.py)
    if 'Resume_str' in data.columns:
        data = data.rename(columns={'Resume_str': 'text'})
    elif 'Resume' in data.columns:
        data = data.rename(columns={'Resume': 'text'})
    else:
        data = data.rename(columns={data.columns[1]: 'text'})

    if 'Category' in data.columns:
        data = data.rename(columns={'Category': 'category'})

    data = data.dropna(subset=['text', 'category'])

    # 2. Split Data (80% for Training, 20% for Testing)
    print("Splitting data into Training (80%) and Testing (20%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        data['text'],
        data['category'],
        test_size=0.2,
        random_state=42
    )

    # 3. Train a Temporary Model
    print("Training model...")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    # 4. Predict on the Test Data
    print("Testing model...")
    predictions = model.predict(X_test_vec)

    # 5. Calculate Accuracy
    accuracy = accuracy_score(y_test, predictions)
    print("\n==============================")
    print(f"MODEL ACCURACY: {accuracy * 100:.2f}%")
    print("==============================")

    # Optional: Detailed Report
    # print("\nDetailed Report:")
    # print(classification_report(y_test, predictions))

except FileNotFoundError:
    print("Error: dataset.csv not found!")
except Exception as e:
    print(f"An error occurred: {e}")