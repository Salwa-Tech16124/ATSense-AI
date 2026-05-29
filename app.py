import streamlit as st
import os
from dotenv import load_dotenv
from utils.text_extractor import extract_text
from utils.nlp_processor import analyze_ats, extract_contact_info
from utils.sarvam_api import get_sarvam_feedback

# Load environment variables
load_dotenv()

st.set_page_config(page_title="ATSense AI | Resume Analyzer & ATS Optimizer", page_icon="✨", layout="wide")

# Theme Toggle
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Sidebar Branding
st.sidebar.title("✨ ATSense AI")
st.sidebar.markdown("---")

# Sidebar Theme Toggle
st.sidebar.markdown("### 🎨 Appearance")
dark_mode_toggle = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode_toggle

# Dynamic CSS Based on Theme Requirements
if st.session_state.dark_mode:
    bg_color = "#0D0D0D"
    card_bg = "#1E1E1E"
    text_color = "#FFFFFF"
    sub_text = "#A3A3A3"
    border_color = "rgba(212, 175, 55, 0.3)"
    gold_color = "#D4AF37"
    gold_gradient = "linear-gradient(135deg, #F3D266 0%, #D4AF37 100%)"
    sidebar_bg = "#121212"
    shadow = "0 8px 32px rgba(0, 0, 0, 0.6)"
    hover_shadow = "0 12px 40px rgba(212, 175, 55, 0.15)"
    input_bg = "#252525"
    uploader_btn_bg = "#333333"
    uploader_btn_text = "#FFFFFF"
else:
    bg_color = "#F7F4EB"
    card_bg = "#FFFFFF"
    text_color = "#1A1A1A"
    sub_text = "#555555"
    border_color = "rgba(184, 134, 11, 0.4)"
    gold_color = "#B8860B"
    gold_gradient = "linear-gradient(135deg, #D4AF37 0%, #B8860B 100%)"
    sidebar_bg = "#EFEBDF"
    shadow = "0 10px 40px rgba(0, 0, 0, 0.08)"
    hover_shadow = "0 15px 50px rgba(184, 134, 11, 0.2)"
    input_bg = "#FFFFFF"
    uploader_btn_bg = "#EBE5D9"
    uploader_btn_text = "#1A1A1A"

st.markdown(f"""
<style>
    /* Base Backgrounds */
    .stApp {{
        background-color: {bg_color};
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border_color};
    }}
    
    /* Typography Overrides to fix visibility in Light Mode */
    h1, h2, h3, h4, h5, h6, p, label, b, strong, li, span {{
        color: {text_color} !important;
    }}
    
    /* Exceptions for typography */
    .sub-header {{
        color: {sub_text} !important;
    }}
    .metric-title {{
        color: {sub_text} !important;
    }}
    .metric-value {{
        color: {gold_color} !important;
    }}
    .section-title {{
        color: {gold_color} !important;
    }}
    .footer {{
        color: {sub_text} !important;
    }}
    
    /* Placeholder text colors for inputs */
    ::-webkit-input-placeholder {{ color: {sub_text} !important; opacity: 0.7; }}
    :-moz-placeholder {{ color: {sub_text} !important; opacity: 0.7; }}
    ::-moz-placeholder {{ color: {sub_text} !important; opacity: 0.7; }}
    :-ms-input-placeholder {{ color: {sub_text} !important; opacity: 0.7; }}
    
    /* Main Header */
    .main-header {{
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.2rem;
        background: {gold_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }}
    .sub-header {{
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 500;
    }}

    /* Premium SaaS Cards */
    .glass-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 24px;
        box-shadow: {shadow};
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }}
    .glass-card:hover {{
        transform: translateY(-5px);
        border: 1px solid {gold_color};
        box-shadow: {hover_shadow};
    }}
    
    .metric-title {{
        font-size: 1.05rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        margin-bottom: 12px;
    }}
    .metric-value {{
        font-size: 3rem;
        font-weight: 900;
        line-height: 1;
    }}

    /* Main CTA Button */
    .stButton > button {{
        background: {gold_gradient} !important;
        color: #FFFFFF !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        font-weight: 800;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(184, 134, 11, 0.4);
        width: 100%;
        font-size: 1.1rem;
    }}
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(184, 134, 11, 0.6);
        filter: brightness(1.1);
    }}
    
    /* Download Button */
    .stDownloadButton > button {{
        background: transparent !important;
        color: {gold_color} !important;
        border: 2px solid {gold_color} !important;
        text-shadow: none;
    }}
    .stDownloadButton > button:hover {{
        background: rgba(184, 134, 11, 0.1) !important;
        color: {gold_color} !important;
    }}

    /* Circular ATS Score Gauge */
    .circular-chart {{
        display: block;
        margin: 10px auto;
        max-width: 80%;
        max-height: 250px;
    }}
    .circle-bg {{
        fill: none;
        stroke: {border_color};
        stroke-width: 2.5;
    }}
    .circle {{
        fill: none;
        stroke-width: 2.5;
        stroke-linecap: round;
        transition: stroke-dasharray 1.5s ease-out;
        stroke: {gold_color};
    }}
    .percentage {{
        fill: {text_color};
        font-family: 'Inter', sans-serif;
        font-size: 0.5em;
        text-anchor: middle;
        font-weight: 900;
    }}
    
    /* Input Fields Overrides */
    .stTextArea textarea {{
        background-color: {input_bg} !important;
        border: 1px solid {border_color} !important;
        color: {text_color} !important;
        border-radius: 12px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }}
    .stTextArea textarea:focus {{
        border-color: {gold_color} !important;
        box-shadow: 0 0 0 2px rgba(184, 134, 11, 0.2) !important;
    }}
    
    /* File Uploader Fixes for Light/Dark Mode */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {input_bg} !important;
        border: 2px dashed {border_color} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stFileUploaderDropzone"]:hover {{
        border-color: {gold_color} !important;
        background-color: rgba(184, 134, 11, 0.02) !important;
    }}
    /* File uploader 'Browse Files' button fix */
    [data-testid="stFileUploaderDropzone"] button {{
        background-color: {uploader_btn_bg} !important;
        color: {uploader_btn_text} !important;
        border: 1px solid {border_color} !important;
        font-weight: bold;
    }}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 15px;
        border-bottom: 2px solid {border_color};
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 55px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 24px;
        color: {sub_text} !important;
        font-weight: 600;
        font-size: 1.05rem;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: rgba(184, 134, 11, 0.08);
        color: {gold_color} !important;
        border-bottom: 3px solid {gold_color};
    }}
    
    /* Typography Utilities */
    .section-title {{
        font-size: 1.7rem;
        font-weight: 800;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid {border_color};
        padding-bottom: 0.8rem;
    }}
    
    /* Tags for skills/keywords */
    .tag {{
        background-color: rgba(184, 134, 11, 0.1);
        color: {gold_color} !important;
        padding: 6px 14px;
        border-radius: 8px;
        margin: 4px;
        display: inline-block;
        font-size: 0.95rem;
        font-weight: 600;
        border: 1px solid rgba(184, 134, 11, 0.3);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .tag-missing {{
        background-color: rgba(220, 38, 38, 0.05) !important;
        color: #DC2626 !important;
        border: 1px solid rgba(220, 38, 38, 0.2) !important;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid {border_color};
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar Content
st.sidebar.markdown("---")
st.sidebar.markdown(f"<h3 style='color: {gold_color}!important; font-weight:800;'>✨ Premium Features</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='line-height: 2;'>
    <b>🎯 Weighted ATS Scoring</b><br>
    <b>🧠 Skill Gap Analysis</b><br>
    <b>🔍 Missing Keyword Detection</b><br>
    <b>💼 Experience & Education Parsers</b><br>
    <b>🤖 Sarvam AI Recruiter Feedback</b><br>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.info("Upload your resume and the job description to get a comprehensive ATS analysis and AI feedback.")
st.sidebar.markdown("---")

# Main Header
st.markdown('<div class="main-header">ATSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Resume Intelligence & ATS Optimization</div>', unsafe_allow_html=True)

# Input Section
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

with col2:
    st.markdown("### 💼 Job Description")
    job_description = st.text_area("Paste the Job Description here", height=150, placeholder="E.g., We are looking for a QA Engineer with 3 years of experience in Python, Selenium...")

st.markdown("<br>", unsafe_allow_html=True)

# Processing Logic
if st.button("🚀 Analyze Resume & Generate Report", use_container_width=True):
    if uploaded_file is not None and job_description:
        with st.spinner("🤖 AI is analyzing your resume against the job description..."):
            resume_text = extract_text(uploaded_file)
            
            if not resume_text:
                st.error("❌ Could not extract text from the uploaded resume. Please try a different file.")
            else:
                analysis_results = analyze_ats(resume_text, job_description)
                contact_info = extract_contact_info(resume_text)
                
                if not analysis_results:
                    st.error("❌ Error analyzing text. Please check inputs.")
                else:
                    ats_score = analysis_results['final_score']
                    category = analysis_results['category']
                    missing_keywords = analysis_results['keywords']['missing_keywords']
                    
                    st.markdown('<div class="section-title">📊 ATS Intelligence Dashboard</div>', unsafe_allow_html=True)
                    
                    # Top Dashboard Row
                    dash_col1, dash_col2 = st.columns([1, 2], gap="large")
                    
                    with dash_col1:
                        # Circular Gauge for ATS Score
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.markdown('<div class="metric-title">ATS Match Score</div>', unsafe_allow_html=True)
                        gauge_html = f"""
                        <svg viewBox="0 0 36 36" class="circular-chart gold">
                          <path class="circle-bg"
                            d="M18 2.0845
                              a 15.9155 15.9155 0 0 1 0 31.831
                              a 15.9155 15.9155 0 0 1 0 -31.831"
                          />
                          <path class="circle"
                            stroke-dasharray="{ats_score}, 100"
                            d="M18 2.0845
                              a 15.9155 15.9155 0 0 1 0 31.831
                              a 15.9155 15.9155 0 0 1 0 -31.831"
                          />
                          <text x="18" y="20.35" class="percentage">{ats_score}%</text>
                        </svg>
                        """
                        st.markdown(gauge_html, unsafe_allow_html=True)
                        st.markdown(f'<div style="color:{gold_color}; font-weight:800; font-size:1.3rem; margin-top:10px;">{category}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with dash_col2:
                        # 4 Sub-metrics in a 2x2 grid
                        m1, m2 = st.columns(2, gap="medium")
                        with m1:
                            st.markdown(f"""
                            <div class="glass-card" style="margin-bottom: 1rem; padding: 1.5rem;">
                                <div class="metric-title">Missing Keywords</div>
                                <div class="metric-value">{len(missing_keywords)}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="glass-card" style="padding: 1.5rem;">
                                <div class="metric-title">Keyword Score (40%)</div>
                                <div class="metric-value">{analysis_results['breakdown']['keyword_score']}%</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with m2:
                            st.markdown(f"""
                            <div class="glass-card" style="margin-bottom: 1rem; padding: 1.5rem;">
                                <div class="metric-title">Missing Skills</div>
                                <div class="metric-value">{len(analysis_results['skills']['missing'])}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="glass-card" style="padding: 1.5rem;">
                                <div class="metric-title">Skill Score (30%)</div>
                                <div class="metric-value">{analysis_results['breakdown']['skill_score']}%</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Detailed Tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["📋 Breakdown & Skills", "🔑 Keyword Analysis", "🤖 AI Recruiter Insights", "🐛 Diagnostics"])
                    
                    with tab1:
                        st.markdown("### 👤 Contact Parsing")
                        st.write(f"📧 **Email:** `{contact_info['email']}`")
                        st.write(f"📞 **Phone:** `{contact_info['phone']}`")
                        
                        st.markdown("### 🎓 Core Requirements (30%)")
                        req1, req2 = st.columns(2)
                        req1.metric("Experience (20%)", f"{analysis_results['breakdown']['exp_score']}%")
                        req2.metric("Education (10%)", f"{analysis_results['breakdown']['edu_score']}%")
                        
                        st.markdown("### 🛠️ Skill Gap Analysis")
                        st.write("**✅ Matched Required Skills:**")
                        if analysis_results['skills']['found']:
                            tags = "".join([f"<span class='tag'>{s.title()}</span>" for s in analysis_results['skills']['found']])
                            st.markdown(tags, unsafe_allow_html=True)
                        else:
                            st.write("No standard required skills matched.")
                            
                        st.write("**❌ Missing Required Skills:**")
                        if analysis_results['skills']['missing']:
                            tags = "".join([f"<span class='tag tag-missing'>{s.title()}</span>" for s in analysis_results['skills']['missing']])
                            st.markdown(tags, unsafe_allow_html=True)
                        else:
                            st.write("Perfect! No missing core skills.")
                            
                        st.write("**📌 Additional Resume Skills Detected:**")
                        extra_skills = set(analysis_results['skills']['resume_skills']) - set(analysis_results['skills']['found'])
                        if extra_skills:
                            tags = "".join([f"<span class='tag' style='background:transparent; border-color:{border_color}; color:{text_color}!important;'>{s.title()}</span>" for s in extra_skills])
                            st.markdown(tags, unsafe_allow_html=True)
                        else:
                            st.write("None.")
                    
                    with tab2:
                        st.markdown("### 🔑 Missing Job Description Keywords")
                        st.write("Incorporate these exact keywords to satisfy older, exact-match ATS systems:")
                        if missing_keywords:
                            tags = "".join([f"<span class='tag tag-missing'>{kw}</span>" for kw in list(missing_keywords)[:40]])
                            st.markdown(tags, unsafe_allow_html=True)
                        else:
                            st.success("Great job! No major missing keywords detected.")
                    
                    with tab3:
                        st.markdown("### 🤖 Sarvam AI Professional Feedback")
                        with st.spinner("Generating intelligent insights..."):
                            ai_feedback = get_sarvam_feedback(resume_text, job_description)
                            st.markdown(f"> {ai_feedback}")
                            
                    with tab4:
                        st.markdown("### 🐛 Engine Diagnostics")
                        st.json({
                            "Skill Extraction": {
                                "JD_Skills": analysis_results['skills']['jd_skills'],
                                "Resume_Skills": analysis_results['skills']['resume_skills'],
                                "Matched_Skills": analysis_results['skills']['found'],
                                "Missing_Skills": analysis_results['skills']['missing']
                            },
                            "Keyword Extraction": {
                                "JD_Keywords": analysis_results['keywords']['jd_keywords'],
                                "Resume_Keywords": analysis_results['keywords']['resume_keywords'],
                                "Matched_Keywords": analysis_results['keywords']['matched_keywords'],
                                "Missing_Keywords": analysis_results['keywords']['missing_keywords']
                            }
                        })
                    
                    # Download Report
                    st.markdown("---")
                    report_content = f"""ATSense AI Report
===========================

ATS Match Score: {ats_score}%
Category: {category}

--- SCORE BREAKDOWN ---
Keywords (40%): {analysis_results['breakdown']['keyword_score']}%
Skills (30%): {analysis_results['breakdown']['skill_score']}%
Experience (20%): {analysis_results['breakdown']['exp_score']}%
Education (10%): {analysis_results['breakdown']['edu_score']}%

--- SKILL GAP ---
Found Skills: {', '.join(analysis_results['skills']['found'])}
Missing Skills: {', '.join(analysis_results['skills']['missing'])}

---------------------------
SARVAM AI PROFESSIONAL FEEDBACK:
{ai_feedback}
"""
                    st.download_button(
                        label="📥 Download ATS Report",
                        data=report_content,
                        file_name="ATSense_AI_Report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

    else:
        st.warning("⚠️ Please upload a resume and provide a job description to begin.")

# Footer
st.markdown('<div class="footer">© 2026 ATSense AI | Built by Salwa Kazmi</div>', unsafe_allow_html=True)
