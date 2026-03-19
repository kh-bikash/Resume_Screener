import streamlit as st
import pandas as pd
from resume_processor import extract_text
from ai_evaluator import evaluate_candidates

st.set_page_config(page_title="AI Resume Screener", page_icon="📝", layout="wide")

st.title("📝 AI Resume Screening System")
st.subheader("Intern Assessment MVP")

with st.sidebar:
    st.header("🔑 Configuration")
    provider = st.selectbox("AI Provider", ["Gemini", "Groq"])
    
    if provider == "Gemini":
        api_key = st.text_input("Google Gemini API Key", type="password", placeholder="AIzaSy...")
        model_name = st.selectbox("LLM Model", ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-2.0-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash-8b"])
        st.info("Get a free key from Google AI Studio.")
    else:
        api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        model_name = st.selectbox("LLM Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
        st.info("Get a free key from console.groq.com/keys.")
        
    if api_key:
        st.success("API Key provided!")

st.markdown("### Job Description")
jd = st.text_area("Paste the Job Description here", height=150)

st.markdown("### Candidate Resumes")
uploaded_files = st.file_uploader("Upload Resumes (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True)

if st.button("🚀 Evaluate Candidates", type="primary"):
    if not api_key:
        st.error("Please provide a Gemini API Key in the sidebar.")
    elif not jd.strip():
        st.error("Please provide a Job Description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        try:
            from ai_evaluator import configure_gemini
            if provider == "Gemini":
                configure_gemini(api_key)
            
            with st.spinner(f"Analyzing candidates with {provider} ({model_name})..."):
                resume_data = []
                for file in uploaded_files:
                    text = extract_text(file)
                    name = file.name.replace(".pdf", "").replace(".txt", "")
                    resume_data.append({"name": name, "text": text})
                
                results = evaluate_candidates(resume_data, jd, provider=provider, model_name=model_name, api_key=api_key)
                
                if not results:
                    st.error("Failed to parse AI response. The prompt may need adjustment.")
                else:
                    st.success("✅ Analysis Complete!")
                    
                    # Converting to dataframe for better results
                    df = pd.DataFrame(results)
                    
                    # Format lists to strings for display if they aren't already
                    if 'strengths' in df.columns:
                        df['strengths'] = df['strengths'].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
                    if 'gaps' in df.columns:
                        df['gaps'] = df['gaps'].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
                    
                    # Sort candidates by score
                    if 'match_score' in df.columns:
                        df = df.sort_values(by="match_score", ascending=False).reset_index(drop=True)
                    
                    # Ensure columns exist and reorder
                    expected_cols_original = ["name", "match_score", "recommendation", "strengths", "gaps"]
                    columns_order = [c for c in expected_cols_original if c in df.columns]
                    df = df[columns_order]
                    
                    # Simple renaming map
                    rename_map = {
                        "name": "Candidate Name",
                        "match_score": "Match Score",
                        "recommendation": "Recommendation",
                        "strengths": "Key Strengths",
                        "gaps": "Key Gaps"
                    }
                    df.rename(columns=rename_map, inplace=True)
                    
                    st.dataframe(df, use_container_width=True)
                    
                    st.markdown("### Detailed Insights")
                    for _, row in df.iterrows():
                        name = row.get("Candidate Name", "Unknown")
                        rec = row.get("Recommendation", "N/A")
                        score = row.get("Match Score", 0)
                        with st.expander(f"{name} - {rec} ({score}/100)"):
                            st.write(f"**Strengths:** {row.get('Key Strengths', 'N/A')}")
                            st.write(f"**Gaps:** {row.get('Key Gaps', 'N/A')}")
                            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")