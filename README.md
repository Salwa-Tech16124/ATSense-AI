
# Project Title

A brief description of what this project does and who it's for

Ran command: `streamlit run app.py
`
Viewed README.md:1-81

Here is a highly polished, GitHub-ready `README.md` file for **ATSense AI**. It includes standard open-source markdown features like badges, a clean layout, table of contents, and placeholders for screenshots. 

You can copy and paste this directly into your GitHub repository!
https://salwa-tech16124-atsense-ai-app-4gr1pc.streamlit.app/

***

```markdown
# ✨ ATSense AI 

<div align="center">
  <h3>AI-Powered Resume Intelligence & ATS Optimization</h3>
  <p>A production-ready AI Resume Analyzer and ATS Score Checker designed to help candidates optimize their resumes against any Job Description using advanced NLP and Generative AI.</p>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/Sarvam_AI-000000?style=for-the-badge&logo=ai&logoColor=white" alt="Sarvam AI" />
</div>

---

## 🌟 Features

* 📄 **Multi-Format Upload:** Extract text flawlessly from `PDF`, `DOCX`, and `TXT` resumes.
* 🎯 **Weighted ATS Scoring Engine:** Calculates a precise match percentage using a 4-part weighted algorithm (40% Keywords, 30% Skills, 20% Experience, 10% Education).
* 🧠 **Skill Gap Analysis:** Extracts required multi-word technical and soft skills and identifies critical gaps.
* 🔍 **Missing Keyword Detection:** Highlights exactly which keywords are missing from your resume to satisfy rigid, legacy ATS systems.
* 🤖 **AI Recruiter Feedback:** Integrates with Sarvam AI to provide intelligent, human-like recruiter feedback and resume improvement suggestions.
* 🎨 **Premium SaaS Dashboard:** Features a beautiful Black & Gold dark/light mode UI with glassmorphism cards and animated circular gauges.
* 📥 **Export Reports:** Download a comprehensive ATS analysis text report with one click.

---

## 📸 Screenshots

*(Add your screenshots here before publishing to GitHub!)*

| Light Theme Dashboard | Dark Theme Dashboard |
| :---: | :---: |
| <img src="URL_TO_LIGHT_THEME_IMAGE" width="400"> | <img src="URL_TO_DARK_THEME_IMAGE" width="400"> |

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python 3.x
* **NLP & Text Processing:** `scikit-learn`, Regex, `PyPDF2`, `python-docx`
* **AI Integration:** Sarvam AI API
* **Environment Management:** `python-dotenv`

---

## 🚀 Setup & Installation

Follow these steps to run ATSense AI locally on your machine.

### 1. Clone the repository
```bash
git clone https://github.com/your-username/atsense-ai.git
cd atsense-ai
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```

**Activate it:**
* **Windows:** `venv\Scripts\activate`
* **macOS/Linux:** `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
1. Rename the provided `.env.example` file to `.env`.
2. Open the `.env` file and securely paste your Sarvam AI API key.
```env
SARVAM_API_KEY=your_sarvam_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```
*The application will automatically open in your default web browser at `http://localhost:8501`.*

---

## 📂 Project Structure

```text
ATSense AI/
├── app.py                  # Main Streamlit application UI
├── requirements.txt        # Python package dependencies
├── .env                    # Environment variables (Do NOT commit this)
├── .env.example            # Template for environment variables
├── README.md               # Project documentation
├── utils/                  # Core logic modules
│   ├── text_extractor.py   # PDF and DOCX parsing logic
│   ├── nlp_processor.py    # ATS scoring, keyword, and skill extraction
│   └── sarvam_api.py       # Sarvam AI API integration & fail-safes
└── samples/                # Sample files for quick testing
    ├── sample_jd.txt       # Example Job Description
    └── sample_resume.txt   # Example Candidate Resume
```

---

## 💡 Usage Example

1. Start the server using the instructions above.
2. In the UI, upload a resume file (you can use `samples/sample_resume.txt`).
3. Paste a Job Description into the text area (you can use `samples/sample_jd.txt`).
4. Click **🚀 Analyze Resume & Generate Report**.
5. Explore your ATS Match Score, missing skills, keyword analysis, and Sarvam AI feedback!

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your-username/atsense-ai/issues).

## 📄 License
This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

---
*Built with ❤️ by Salwa Kazmi*
```
