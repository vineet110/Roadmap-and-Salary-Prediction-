import streamlit as st
import pickle
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
import os

from utils import analyze_profile, generate_roadmap
from shap_explainer import get_shap_values
from auth import login, register
from jobs_api import fetch_jobs
from ai_roadmap import generate_ai_roadmap
from report_generator import generate_pdf

# ================= LOAD CSS =================
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ================= LOAD MODEL =================
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Career AI", layout="wide")

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= AUTH =================
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Login":
        if st.sidebar.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.success("Welcome 🚀")
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Register":
        if st.sidebar.button("Register"):
            if register(username, password):
                st.success("User created")
                st.rerun()
            else:
                st.error("User exists")

    st.stop()

# ================= MAIN =================

st.title("🚀 AI Career Intelligence Dashboard")
st.sidebar.success("Logged in")

# ================= INPUT =================
projects = st.sidebar.slider("Projects", 0, 10, 2)
internships = st.sidebar.slider("Internships", 0, 5, 0)
cgpa = st.sidebar.slider("CGPA", 5.0, 10.0, 7.5)
certifications = st.sidebar.slider("Certifications", 0, 10, 1)
coding_score = st.sidebar.slider("Coding Score", 0, 100, 50)

skills = st.sidebar.multiselect("Skills", ["DSA", "Web Dev", "ML", "Cloud"])
target_role = st.sidebar.selectbox("Target Role", ["SDE", "ML Engineer", "Data Scientist"])

# ================= ANALYZE =================
if st.sidebar.button("Analyze Profile"):

    input_data = np.array([[projects, internships, cgpa, certifications, coding_score]])
    salary = model.predict(input_data)[0]

    # 🔥 SAFETY FIX
    if salary > 100:
        salary = salary / 1000

    low, high = salary * 0.8, salary * 1.2

    # ================= ROW 1 =================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💰 Salary Prediction</div>', unsafe_allow_html=True)
        st.metric("Predicted Salary", f"{salary:.2f} LPA")
        st.markdown(f'<div class="highlight">Range: {low:.2f} - {high:.2f} LPA</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    data = {
        "projects": projects,
        "internships": internships,
        "cgpa": cgpa,
        "coding_score": coding_score,
        "skills": skills,
        "target_role": target_role
    }

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Profile Analysis</div>', unsafe_allow_html=True)

        issues = analyze_profile(data)

        if issues:
            for i in issues:
                st.markdown(f'<div class="warning-box">⚠ {i}</div>', unsafe_allow_html=True)
        else:
            st.success("Strong profile 💪")

        st.markdown('</div>', unsafe_allow_html=True)

    # ================= ROADMAP =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🛣️ Rule-Based Roadmap</div>', unsafe_allow_html=True)

    roadmap = generate_roadmap(data)
    for step in roadmap:
        st.write("•", step)

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= AI ROADMAP =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🤖 AI Generated Roadmap</div>', unsafe_allow_html=True)

    ai_plan = generate_ai_roadmap(data)
    st.write(ai_plan)

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= SHAP =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Feature Importance</div>', unsafe_allow_html=True)

    try:
        shap_values = get_shap_values(input_data)

        fig = plt.figure()
        shap.summary_plot(shap_values, input_data, show=False)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"SHAP Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= JOBS =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Live Jobs</div>', unsafe_allow_html=True)

    try:
        for job in fetch_jobs(target_role):
            st.write("•", job)
    except:
        st.warning("Could not fetch jobs")

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= PDF DOWNLOAD =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 Download Report</div>', unsafe_allow_html=True)

    pdf_file = generate_pdf(data, salary, roadmap, ai_plan)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="Download PDF Report",
            data=f,
            file_name="career_report.pdf",
            mime="application/pdf"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= SAVE HISTORY =================
    pd.DataFrame([{
        "projects": projects,
        "internships": internships,
        "cgpa": cgpa,
        "salary": salary
    }]).to_csv("history.csv", mode="a", header=False, index=False)

# ================= HISTORY DASHBOARD =================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Profile History</div>', unsafe_allow_html=True)

if os.path.exists("history.csv"):
    df_hist = pd.read_csv("history.csv")

    st.dataframe(df_hist.tail(10))

    if "salary" in df_hist.columns:
        st.line_chart(df_hist["salary"])
else:
    st.write("No history yet")

st.markdown('</div>', unsafe_allow_html=True)