
# 🚀 Automated Meeting Minutes Generator (Insurance Claims Committee)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)](https://streamlit.io/)  
[![Groq LLaMA](https://img.shields.io/badge/AI-Groq%20LLaMA-6f42c1)](https://groq.com/)  
[![Whisper](https://img.shields.io/badge/Audio-Whisper-green)](https://openai.com/research/whisper)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  

> A secure, GenAI-powered tool that **automatically generates accurate, structured, and editable Minutes of Meetings (MoM)** from **audio recordings, transcripts, PDFs, and images**.  
> Built for **Insurance Claims Review Committees**, but extensible to any business/organization meetings.

---

## 📖 Table of Contents
1. [✨ Features](#-features)  
2. [🧩 Architecture](#-architecture)  
3. [📦 Tech Stack](#-tech-stack)  
4. [🚀 Usage](#-usage)  
5. [📂 Project Structure](#-project-structure)  
6. [🔐 Security & Compliance](#-security--compliance)  
7. [🛠️ Roadmap](#️-roadmap)  
8. [🤝 Contributing](#-contributing)  
=  

---

## ✨ Features
✅ **Multi-Input Support** – Upload audio, text, PDFs, or images  
✅ **AI-Powered Summarization** – Groq LLaMA generates structured MoMs  
✅ **Audio Transcription** – OpenAI Whisper converts speech to text  
✅ **OCR Extraction** – Extract text from scanned PDFs/images  
✅ **Downloadable & Editable Output** – Export MoMs as `.docx`, `.txt`, or `.pdf` (via `fpdf2`)  
✅ **Secure & Compliant** – Handles sensitive insurance data safely  
✅ **Change Logs** – Track edits with timestamps  
✅ **Streamlit UI** – Minimal, clean, and user-friendly  

---

## 🧩 Architecture


	•	Input Layer: Upload audio, PDF, images, or text
	•	Preprocessing: Whisper → Text | OCR → Text
	•	AI Summarization: LLaMA generates MoM sections (Agenda, Discussions, Decisions, Action Items)
	•	Output Layer: Editable + downloadable
	•	UI Layer: Streamlit web app
	•	Security: Local storage, optional encryption, logs



## 📦 Tech Stack

| Layer            | Tools / Tech            |
|------------------|--------------------------|
| Frontend         | Streamlit               |
| Summarization    | Groq LLaMA API          |
| Audio Transcribe | OpenAI Whisper          |
| OCR              | pytesseract + pdfplumber|
| Output           | fpdf2, python-docx, Markdown |
| Backend Logic    | Python                  |
| Storage & Logs   | SQLite / JSON           |




5️⃣ Run the app
```
streamlit run App.py
```

⸻

## 🚀 Usage
	1.	Upload your meeting file (.mp3, .wav, .txt, .pdf, .jpg, .png)
	2.	The system transcribes or extracts text
	3.	AI (Groq LLaMA) generates structured MoM under headings:
	•	Agenda
	•	Discussions
	•	Decisions Taken
	•	Action Items
	4.	Preview the MoM inside the app
	5.	Edit if needed
	6.	Download as .docx, .pdf, or .txt

⸻

📂 Project Structure
```
project-root/
│
├── app/
│   ├── main.py                # Streamlit entry point
│   ├── utils/
│   │   ├── ocr.py             # OCR utilities
│   │   ├── whisper_transcribe.py  # Audio transcription
│   │   ├── summarizer.py      # Groq LLaMA summarization
│   │   ├── file_handler.py    # File operations
│   │   └── logger.py          # Logging edits
│   └── components/
│       ├── uploader.py        # File upload UI
│       └── editor.py          # MoM editor
│
├── data/
│   ├── transcripts/           # Raw transcripts
│   ├── outputs/               # Generated MoMs
│   └── logs/                  # Change logs
│
├── models/
│   ├── whisper_model.py
│   └── groq_prompt.py
│
├── requirements.txt
├── README.md
└── .env
```

⸻


## 🔐 Security & Compliance
	•	✅ Encrypted file storage (optional)
	•	✅ Auto-cleanup of uploaded files after session
	•	✅ No external file sharing except secure API calls
	•	✅ Edit logs maintained with timestamps
	•	✅ Role-based access control (planned for Phase 2)

⸻

## 🛠️ Roadmap
	•	Phase 1 – Core system (Current release)
	•	Phase 2 – Role-based login, cloud deployment (GCP/AWS), multilingual support
	•	Phase 3 – Deeper summarization (meeting sentiment, follow-up tasks)

⸻

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
	1.	Fork the project
	2.	Create your feature branch =
	3.	Commit changes =
