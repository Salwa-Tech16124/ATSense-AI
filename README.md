# ATSense AI 📄🤖

**ATSense AI: AI-Powered Resume Intelligence & ATS Optimization**

ATSense AI is a complete, production-ready AI Resume Analyzer and ATS Score Checker. It uses Python, Streamlit, NLP techniques, and the Sarvam AI API to provide comprehensive feedback on a candidate's resume relative to a target job description.

## 🌟 Features
1. **Upload Resume:** Supports PDF, DOCX, and TXT files.
2. **Paste Job Description:** Easily paste target job requirements.
3. **Extract Resume Text:** Seamless extraction of content from complex documents.
4. **ATS Score Calculation:** Uses a Weighted ATS Scoring System (Keywords, Skills, Experience, Education) to calculate a precise match percentage.
5. **Missing Keyword Detection:** Identifies critical keywords present in the JD but missing in the resume.
6. **Skills, Education, & Experience Extraction:** Core details are automatically categorized.
7. **Contact Information Extraction:** Automatically finds emails and phone numbers.
8. **Modern ATS Dashboard:** Beautiful Streamlit UI with progress bars and metrics.
9. **Download ATS Report:** Export your personalized feedback as a text file.
10. **Sarvam AI Integration:** Provides intelligent recruiter feedback, skill gap analysis, and resume improvement suggestions.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **NLP & ML:** Scikit-learn, Regex
- **File Processing:** PyPDF2, python-docx
- **AI Integration:** Sarvam AI API
- **Environment Management:** python-dotenv

## 🚀 Step-by-Step Setup Guide

### 1. Clone the repository (or extract the project folder)
Ensure you are in the project root directory.

### 2. Create a virtual environment (Recommended)
```bash
python -m venv venv
```
Activate it:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
- Copy the `.env.example` file and rename it to `.env`.
- Paste your Sarvam AI API key into the `.env` file:
```
SARVAM_API_KEY=your_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```
This will start the local server and open the app in your default web browser!

## 📂 Folder Structure
```
ATSense AI/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (API Key)
├── .env.example            # Template for environment variables
├── README.md               # Project documentation
├── utils/                  # Helper modules
│   ├── __init__.py
│   ├── text_extractor.py   # PDF and DOCX parsing
│   ├── nlp_processor.py    # ATS scoring and keyword extraction
│   └── sarvam_api.py       # Sarvam AI API integration
└── samples/                # Sample files for testing
    ├── sample_jd.txt
    └── sample_resume.txt
```

## 💡 Usage Example
1. Run the app.
2. Upload `samples/sample_resume.txt`.
3. Paste the contents of `samples/sample_jd.txt` into the Job Description box.
4. Click **Analyze Resume** and explore the dashboard!
