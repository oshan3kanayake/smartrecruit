import pandas as pd
from collections import Counter
import os

# 1. Load Data
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'dataset.csv')

try:
    print("--- DIAGNOSIS REPORT ---")
    data = pd.read_csv(csv_path)

    # 2. Fix Columns (Same logic as before)
    if 'Resume_str' in data.columns:
        data = data.rename(columns={'Resume_str': 'text'})
    elif 'Resume' in data.columns:
        data = data.rename(columns={'Resume': 'text'})
    else:
        data = data.rename(columns={data.columns[1]: 'text'})

    if 'Category' in data.columns:
        data = data.rename(columns={'Category': 'category'})

    data = data.dropna(subset=['text', 'category'])

    # 3. Print Stats
    print(f"1. Total Resumes Found: {len(data)}")

    print("\n2. Top 5 Categories (Job Titles):")
    counts = Counter(data['category'])
    for job, count in counts.most_common(5):
        print(f"   - {job}: {count} resumes")

    print(f"\n3. Number of Unique Categories: {len(counts)}")

    print("\n4. Sample Text (First 100 chars of row 1):")
    print(f"   \"{str(data.iloc[0]['text'])[:100]}...\"")

    if len(data) < 50:
        print("\n⚠️ WARNING: Your dataset is VERY SMALL. This explains the low accuracy.")
        print("   Did you forget to replace the manual dataset with the Kaggle one?")
    else:
        print("\n✅ Dataset size looks good.")

except Exception as e:
    print(f"Error: {e}")