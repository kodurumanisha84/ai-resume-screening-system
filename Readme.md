# 💼 AI Resume Screening System (ATS Dashboard)

## 🚀 Overview

The **AI Resume Screening System** is an advanced Applicant Tracking System (ATS)-style web application that automates resume evaluation using Natural Language Processing (NLP) and Machine Learning techniques.

It allows recruiters to upload a job description and multiple resumes, then intelligently:

* Analyzes candidate profiles
* Matches skills with job requirements
* Calculates a relevance score
* Ranks candidates
* Explains **why candidates are shortlisted or rejected**

---

## 🎯 Problem Statement

Recruiters often spend hours manually reviewing resumes. This process is:

* Time-consuming
* Inconsistent
* Prone to human bias

This project solves the problem by:

* Automating resume screening
* Standardizing evaluation
* Providing explainable insights

---

## 💡 Key Features

### 🧠 AI-Based Screening

* TF-IDF + Cosine Similarity for semantic matching
* Skill extraction and comparison
* Experience-based scoring

### 🎯 Intelligent Scoring System

Final score is calculated using:

* Similarity Score
* Skill Match Percentage
* Experience Score
* Penalty for missing must-have skills

### 📊 Interactive Dashboard

Built using Streamlit:

* Upload Job Description & Resumes
* Real-time analysis
* Candidate ranking table
* Filters & search functionality

### 📈 Visual Analytics

* Candidate score comparison (bar chart)
* Score distribution (histogram)
* Score breakdown (scatter plot)

### 🧠 Explainable AI

For each candidate:

* Matched skills
* Missing skills
* Experience analysis
* Clear rejection reasons

### 🏆 Top Candidate Identification

Highlights the best candidate with:

* Score
* Skills
* Experience

### 📥 Export Results

* Download results as CSV

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (Dashboard UI)
* **Pandas & NumPy** (Data Processing)
* **Scikit-learn** (TF-IDF & Cosine Similarity)
* **pdfplumber** (PDF text extraction)
* **Plotly** (Interactive visualizations)
* **Regex (re)** (Text processing)

---

## 📂 Project Structure

```
Automated-Resume-Screening-Tool/
│
├── app.py                  # Main Streamlit dashboard
├── main.py                 # (Optional) CLI version
├── requirements.txt
├── README.md
│
├── resumes/                # Sample resumes
│   ├── resume1.pdf
│   ├── resume2.pdf
│
├── outputs/                # Generated results
│   ├── final_results.csv
│
├── images/                 # Screenshots
│   ├── dashboard.png
│   ├── results.png
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-resume-screening-system.git
cd ai-resume-screening-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Then open the browser:

```
http://localhost:8501
```

---

## 🧪 How It Works

1. Upload Job Description
2. Upload multiple resumes
3. System extracts text from PDFs
4. NLP model compares resumes with JD
5. Calculates scores
6. Ranks candidates
7. Shows insights & explanations

---

## 📊 Sample Output

* Candidate Ranking Table
* Score Visualization
* Shortlisted vs Rejected
* Explainability Panel

---

## 📸 Screenshots

*Add your screenshots here:*

* Dashboard UI
* Candidate Ranking
* Charts
* Explanation Panel

---

## 🧠 Learning Outcomes

* NLP-based text processing
* TF-IDF and cosine similarity
* Resume parsing techniques
* Dashboard development using streamlit
* Building explainable AI systems
* Real-world problem solving

---

## 💼 Industry Relevance

This project simulates real ATS systems used by:

* HR teams
* Recruitment platforms
* Hiring managers

It demonstrates skills relevant for:

* Data Analyst
* Machine Learning Engineer
* Python Developer
* HR Tech roles

---

## 🔮 Future Enhancements

* FastAPI backend integration
* Database (SQLite/PostgreSQL)
* Resume parsing using NLP libraries (spaCy)
* Authentication system

---

## 🙋‍♀️ Author

**Koduru Manisha**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!
