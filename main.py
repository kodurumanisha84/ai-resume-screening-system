import os
import pandas as pd
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# Load Job Description
# ---------------------------
job_file_path = os.path.join("data", "job_description.txt")

if not os.path.exists(job_file_path):
    print("❌ Job description file not found!")
    exit()

with open(job_file_path, "r", encoding="utf-8") as f:
    job_desc = f.read()

print("✅ Job description loaded successfully\n")

# ---------------------------
# Extract text from PDF
# ---------------------------
def extract_text(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return text.strip()

# ---------------------------
# Load Resumes
# ---------------------------
resume_folder = os.path.abspath("resumes")

if not os.path.exists(resume_folder):
    print("❌ 'resumes' folder not found!")
    exit()

resume_texts = []
resume_names = []

print("📂 Reading resumes...\n")

for file in os.listdir(resume_folder):
    if file.lower().endswith(".pdf"):
        file_path = os.path.join(resume_folder, file)

        print(f"➡ Processing: {file}")

        text = extract_text(file_path)

        if text:
            resume_texts.append(text)
            resume_names.append(file)
        else:
            print(f"⚠ Warning: No text extracted from {file}")

# Check if resumes exist
if len(resume_texts) == 0:
    print("❌ No valid resumes found. Please add PDF resumes.")
    exit()

# ---------------------------
# TF-IDF Vectorization
# ---------------------------
print("\n🔍 Calculating similarity...\n")

documents = [job_desc] + resume_texts

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)

# ---------------------------
# Cosine Similarity
# ---------------------------
job_vector = tfidf_matrix[0]
resume_vectors = tfidf_matrix[1:]

scores = cosine_similarity(job_vector, resume_vectors)[0]

# ---------------------------
# Create DataFrame
# ---------------------------
df = pd.DataFrame({
    "Resume": resume_names,
    "Score": scores
})

# Sort by score
df = df.sort_values(by="Score", ascending=False)

# ---------------------------
# Shortlist Logic
# ---------------------------
threshold = 0.3

df["Status"] = df["Score"].apply(
    lambda x: "Shortlisted" if x >= threshold else "Rejected"
)

# ---------------------------
# Save Output
# ---------------------------
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(output_folder, "results.csv")
df.to_csv(output_path, index=False)

# ---------------------------
# Display Results
# ---------------------------
print("✅ Final Results:\n")
print(df)

print(f"\n📁 Results saved at: {output_path}")