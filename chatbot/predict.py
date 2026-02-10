import sys
import pickle
import os
import re
from sklearn.metrics.pairwise import cosine_similarity

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'recruitment_model.pkl')

def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text.lower())

try:
    if len(sys.argv) < 2:
        print("0")
        sys.exit()

    raw_input = sys.argv[1]

    if "|||SEPARATOR|||" in raw_input:
        parts = raw_input.split("|||SEPARATOR|||")
        job_text = clean_text(parts[0])
        resume_text = clean_text(parts[1])
    else:
        print("0")
        sys.exit()

    with open(model_path, 'rb') as f:
        vectorizer, model = pickle.load(f)

    # Calculate Similarity
    vectors = vectorizer.transform([job_text, resume_text])
    similarity = cosine_similarity(vectors)[0][1]

    # Score Logic
    final_score = int(similarity * 100)

    # Scaling for user friendliness
    if final_score < 10:
        final_score = 15
    elif final_score < 30:
        final_score = final_score + 25
    else:
        final_score = min(final_score + 35, 98)

    # ONLY PRINT THE NUMBER
    print(f"{final_score}")

except Exception as e:
    print("0")