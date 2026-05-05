import streamlit as st
import pdfplumber
import pandas as pd
import re
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="ATS Resume Screener", layout="wide")

# ---------------------------
# HEADER
# ---------------------------
st.title("💼 AI Resume Screening System")
st.markdown("### Professional Recruiter Dashboard with Explainable AI")

# ---------------------------
# SKILLS CONFIG
# ---------------------------
MUST_HAVE = ["python", "sql", "excel"]
NICE_TO_HAVE = ["machine learning", "power bi", "tableau"]
ALL_SKILLS = MUST_HAVE + NICE_TO_HAVE

# ---------------------------
# FILE UPLOAD
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    jd_file = st.file_uploader("📄 Upload Job Description", type=["txt", "pdf"])

with col2:
    resumes = st.file_uploader("📂 Upload Resumes", type=["pdf"], accept_multiple_files=True)

# ---------------------------
# FUNCTIONS
# ---------------------------
def extract_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except:
        pass
    return text.lower()

def extract_text(file):
    if file.name.endswith(".pdf"):
        return extract_pdf(file)
    return file.read().decode("utf-8").lower()

def extract_skills(text):
    return list(set([s for s in ALL_SKILLS if s in text]))

def extract_experience(text):
    match = re.findall(r'(\d+)\s+years', text)
    return max([int(x) for x in match]) if match else 0

def highlight_score(val):
    if val > 70:
        return "background-color: #c8e6c9"
    elif val > 40:
        return "background-color: #fff9c4"
    else:
        return "background-color: #ffcdd2"

# ---------------------------
# MAIN PROCESS
# ---------------------------
if st.button("🔍 Analyze Candidates"):

    if not jd_file or not resumes:
        st.warning("⚠ Please upload both Job Description and Resumes")
    else:
        jd_text = extract_text(jd_file)

        results = []

        for file in resumes:
            text = extract_pdf(file)

            if text.strip() == "":
                continue

            # Similarity
            tfidf = TfidfVectorizer(stop_words="english")
            matrix = tfidf.fit_transform([jd_text, text])
            sim = float(cosine_similarity(matrix[0], matrix[1])[0][0])

            # Skills
            skills = extract_skills(text)
            skill_match = len(set(skills) & set(ALL_SKILLS)) / max(len(ALL_SKILLS),1)

            must_match = len(set(skills) & set(MUST_HAVE))
            missing_must = list(set(MUST_HAVE) - set(skills))

            # Experience
            exp = extract_experience(text)
            exp_score = min(exp / 3, 1)

            # Penalty
            penalty = 0.15 * len(missing_must)

            # Final Score (SAFE CLAMP)
            raw_score = (0.5 * sim) + (0.3 * skill_match) + (0.2 * exp_score) - penalty
            final_score = max(0, min(raw_score, 1))

            # Reasons
            reasons = []
            if sim < 0.3:
                reasons.append("Low similarity")
            if missing_must:
                reasons.append(f"Missing must-have: {', '.join(missing_must)}")
            if exp < 2:
                reasons.append("Low experience")

            decision = "Shortlisted" if final_score > 0.4 else "Rejected"

            results.append({
                "Name": file.name,
                "Final Score": round(final_score, 2),
                "Similarity": round(sim, 2),
                "Skill Match (%)": round(skill_match * 100, 1),
                "Experience (Years)": exp,
                "Decision": decision,
                "Reasons": "; ".join(reasons) if reasons else "Strong Profile",
                "Matched Skills": ", ".join(set(skills) & set(ALL_SKILLS)),
                "Missing Must-Have": ", ".join(missing_must)
            })

        df = pd.DataFrame(results)

        if df.empty:
            st.error("❌ No valid resumes processed")
            st.stop()

        # Convert numeric safely
        for col in ["Final Score", "Similarity", "Skill Match (%)"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()
        df = df.sort_values(by="Final Score", ascending=False)

        # Add percentage
        df["Final Score (%)"] = (df["Final Score"] * 100).round(1)

        # ---------------------------
        # KPI METRICS
        # ---------------------------
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Candidates", len(df))
        c2.metric("Shortlisted", len(df[df["Decision"] == "Shortlisted"]))
        c3.metric("Rejected", len(df[df["Decision"] == "Rejected"]))

        # ---------------------------
        # TOP CANDIDATE
        # ---------------------------
        top = df.iloc[0]

        st.markdown(f"""
        ## 🏆 Top Candidate: {top['Name']}

        - 🎯 Score: **{top['Final Score (%)']}%**
        - 🧠 Skills: {top['Matched Skills']}
        - ⚠ Missing: {top['Missing Must-Have']}
        - 📊 Experience: {top['Experience (Years)']} years
        """)

        # ---------------------------
        # SEARCH + FILTER
        # ---------------------------
        st.subheader("🔍 Filter Candidates")

        search = st.text_input("Search Candidate")
        threshold = st.slider("Minimum Score", 0.0, 1.0, 0.4)

        filtered_df = df[df["Final Score"] >= threshold]

        if search:
            filtered_df = filtered_df[
                filtered_df["Name"].str.contains(search, case=False)
            ]

        # ---------------------------
        # TABLE WITH COLOR
        # ---------------------------
        st.subheader("📊 Candidate Ranking")

        def color_score(val):
            if val >= 70:
               return "🟢"
            elif val >= 40:
                return "🟡"
            else:
                 return "🔴"

        filtered_df["Score Indicator"] = filtered_df["Final Score (%)"].apply(color_score)

        st.dataframe(filtered_df, use_container_width=True)

        # ---------------------------
        # CHARTS
        # ---------------------------
        st.subheader("📊 Candidate Scores")

        fig_bar = px.bar(
            filtered_df,
            x="Name",
            y="Final Score (%)",
            color="Decision",
            text="Final Score (%)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("📈 Score Distribution")

        fig_hist = px.histogram(df, x="Final Score (%)", nbins=10)
        st.plotly_chart(fig_hist, use_container_width=True)

        st.subheader("📊 Score Breakdown")

        safe_df = df.copy()
        safe_df["Final Score"] = safe_df["Final Score"].clip(lower=0.01)

        fig_scatter = px.scatter(
            safe_df,
            x="Similarity",
            y="Skill Match (%)",
            size="Final Score",
            color="Decision",
            hover_name="Name"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # ---------------------------
        # INSIGHTS
        # ---------------------------
        st.subheader("📌 Insights")

        st.write(f"📊 Average Score: {round(df['Final Score (%)'].mean(),1)}%")
        st.write(f"🏆 Best Score: {round(df['Final Score (%)'].max(),1)}%")

        # ---------------------------
        # EXPLAINABILITY
        # ---------------------------
        st.subheader("🧠 Candidate Explanation")

        for _, row in df.iterrows():
            with st.expander(f"{row['Name']} - {row['Decision']}"):
                st.write(f"Score: {row['Final Score (%)']}%")
                st.write(f"Similarity: {row['Similarity']}")
                st.write(f"Skill Match: {row['Skill Match (%)']}%")
                st.write(f"Experience: {row['Experience (Years)']} years")
                st.write(f"Matched Skills: {row['Matched Skills']}")
                st.write(f"Missing Must-Have: {row['Missing Must-Have']}")
                st.write(f"Reason: {row['Reasons']}")

        # ---------------------------
        # DOWNLOAD
        # ---------------------------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Report", csv, "final_results.csv")