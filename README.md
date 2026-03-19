# 🚀 AI Resume Screening System (MVP)

![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-API-orange?style=for-the-badge&logo=google&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Fast_Inference-black?style=for-the-badge)

A powerful, automated AI-driven Resume Screening System built as a production-ready MVP. It leverages LLMs (Google Gemini & Groq) to evaluate multiple resumes against a Job Description, extracting deep insights and providing an immediate ranked dashboard of candidates.

## 🎯 Features
- **Dynamic AI Provider Selection**: Seamlessly switch between Google Gemini and Groq depending on your API key.
- **Multi-Format Support**: Easily parse structured data from both **PDF** and **TXT** files.
- **Intelligent Scoring**: Calculates a rigorous 0-100 match score based on Skills, Experience, and Education Fit.
- **Actionable Insights**: Instantly extracts top 3 **Strengths** and **Gaps** for every candidate.
- **Dashboard UI**: Built with Streamlit for a highly reactive, user-friendly sorting dashboard.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kh-bikash/Resume_Screener.git
cd Resume_Screener
```

### 2. Install Dependencies
Make sure you have Python 3.9+ installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```
*The app will automatically open in your browser at `http://localhost:8501`.*

---

## 💡 How to Use
1. **Configure AI:** Open the sidebar, select your preferred provider (Gemini or Groq), and paste your API key.
2. **Job Description:** Paste the hiring requirements into the text area.
3. **Upload Resumes:** Drag and drop candidate resumes into the file uploader. (A `sample_data/` folder is provided with 5 test resumes out-of-the-box!)
4. **Evaluate:** Click the "Evaluate Candidates" button to generate your dashboard.

---

## 🌐 Live Deployment
This application is designed to be easily deployable on Streamlit Community Cloud. 
1. Push this code to GitHub.
2. Connect the repository at [share.streamlit.io](https://share.streamlit.io/)
3. Click "Deploy" to generate a public link.

---
*Built for the AI Automation Intern Assessment.*
