import streamlit as st
from app.components.uploader import file_uploader_component
from app.utils.file_handler import handle_uploaded_file, consolidate_text, export_docx, export_pdf
from app.utils.whisper_transcribe import transcribe_audio
from app.utils.ocr import extract_text_ocr
from app.utils.summarizer_llama import generate_mom
from app.utils.logger import log_event, get_logs
from app.components.editor import editor_component
import os
from dotenv import load_dotenv

# --- PAGE CONFIGURATION & BACKEND SETUP ---
load_dotenv()
st.set_page_config(
    page_title="Automated MoM Generator",
    page_icon="✍️",
    layout="centered"
)

# --- INJECT CUSTOM CSS FOR A FORCED DARK MODE UI ---
def load_css():
    css = """
    <style>
        /* --- Font & Animations --- */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- Forced Dark Theme Variables --- */
        :root {
            --primary-color: #19A7CE;       /* Bright Cyan for accents */
            --secondary-color: #4A90E2;     /* A calm blue for secondary elements */
            --background-color: #0E1117;    /* Deep charcoal - Streamlit's dark bg */
            --card-background: #161B22;     /* Slightly lighter charcoal for cards */
            --text-color: #FAFAFA;          /* Off-white for readability */
            --subtle-text-color: #A0AEC0;   /* Grey for subtitles and placeholders */
            --border-color: #30363D;        /* Subtle border color */
        }

        /* --- Main App Styling --- */
        body {
            font-family: 'Roboto', sans-serif;
            color: var(--text-color);
        }
        .stApp {
            background-color: var(--background-color);
        }

        /* --- Custom Containers & Cards --- */
        .main-container {
            animation: fadeIn 0.5s ease-in-out;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            background-color: var(--card-background);
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }

        /* --- Title & Header Styling --- */
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        .sub-header {
            text-align: center;
            color: var(--subtle-text-color);
            margin-bottom: 2rem;
        }
        .section-title {
            font-size: 1.75rem;
            font-weight: 500;
            color: var(--primary-color);
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--primary-color);
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        /* --- Button Styling --- */
        .stButton > button {
            border-radius: 8px;
            border: 2px solid var(--primary-color);
            color: var(--primary-color);
            background-color: transparent;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: var(--primary-color);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(25, 167, 206, 0.3);
        }
        .stButton > button:disabled {
            border-color: var(--border-color);
            color: var(--subtle-text-color);
            background-color: transparent;
        }
        
        /* Smaller buttons (save, download) */
        .stDownloadButton > button, .small-btn > button {
             font-size: 0.9rem;
             padding: 0.5rem 1rem;
             width: auto;
        }
        .small-btn > button {
            border: 2px solid var(--secondary-color);
            color: var(--secondary-color);
        }
        .small-btn > button:hover {
            background-color: var(--secondary-color);
            color: white;
            box-shadow: 0 2px 6px rgba(74, 144, 226, 0.3);
        }
        
        /* --- Placeholder Styling --- */
        .placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 3rem;
            text-align: center;
            border: 2px dashed var(--border-color);
            border-radius: 12px;
        }
        .placeholder-text {
            font-size: 1.1rem;
            color: var(--subtle-text-color);
            margin-top: 1rem;
        }
        
        /* --- Make Streamlit elements like st.info adapt --- */
        .stAlert {
            border-radius: 8px;
        }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


if "mom_generated" not in st.session_state:
    st.session_state.mom_generated = False
    st.session_state.summary = ""
    st.session_state.file_info = {}
    st.session_state.updated_summary = ""

load_css()


st.markdown("<h1 class='main-title'>Automated Meeting Minutes Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Upload your meeting files to instantly generate professional, editable Minutes of Meeting.</p>", unsafe_allow_html=True)


st.markdown("<h2 class='section-title'>Transcription Settings</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    selected_language = st.selectbox(
        "Select meeting language:",
        ["English", "Hindi", "Tamil"],
        index=0
    )

with col2:
    transcription_mode = st.selectbox(
        "Transcription Output:",
        ["Keep in same language", "Translate to English"],
        index=0
    )
    
with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    uploaded_file, participant_tag, manual_participant_entry = file_uploader_component()
    btn_pressed = st.button("Process & Generate MoM", disabled=not uploaded_file)
    st.markdown("</div>", unsafe_allow_html=True)


if btn_pressed:
    with st.spinner("Processing your file... This may take a moment."):
        os.makedirs("./data/transcripts/", exist_ok=True)
        os.makedirs("./data/outputs/", exist_ok=True)
        os.makedirs("./data/logs/", exist_ok=True)
        file_info = handle_uploaded_file(uploaded_file)
        file_path, ext = file_info["filepath"], file_info["ext"]
        st.session_state.file_info = file_info
        text = ""
        if ext in [".mp3", ".wav"]:
            # Map language selection to Whisper codes
            lang_map = {"English": "en", "Hindi": "hi", "Tamil": "ta"}
            language_code = lang_map.get(selected_language, "en")

            # Task selection: transcribe or translate
            task = "transcribe" if transcription_mode == "Keep in same language" else "translate"

            text = transcribe_audio(file_path, language=language_code, task=task)

            # If user kept Hindi/Tamil and not translated
            if transcription_mode == "Keep in same language" and language_code != "en":
                st.warning("⚠️ Summarization may be inaccurate since LLaMA works best with English. Consider using 'Translate to English'.")
        elif ext in [".pdf", ".jpg", ".jpeg", ".png"]:
            text = extract_text_ocr(file_path)
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        transcript_path = consolidate_text(text)
        summary = generate_mom(text, participants=participant_tag or manual_participant_entry)
        st.session_state.summary = summary
        st.session_state.updated_summary = summary
        output_file_path = f"./data/outputs/meeting_{file_info['timestamp']}.md"
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(summary)
        st.session_state.output_file_path = output_file_path
        log_event({
            "event": "MoM Generated",
            "timestamp": file_info["timestamp"],
            "participants": participant_tag or manual_participant_entry,
            "filename": file_info["filename"]
        })
        st.session_state.mom_generated = True
        st.rerun()


if st.session_state.mom_generated:
    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Generated Minutes of Meeting</h2>", unsafe_allow_html=True)
        st.info("The text below is fully editable. Make your changes and click 'Save Edits'.", icon="✍️")
        
        edited_summary = editor_component(st.session_state.updated_summary)
        if edited_summary != st.session_state.updated_summary:
            st.session_state.updated_summary = edited_summary
            
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown('<div class="small-btn">', unsafe_allow_html=True)
            if st.button("Save Edits"):
                with open(st.session_state.output_file_path, "w", encoding="utf-8") as f:
                    f.write(st.session_state.updated_summary)
                log_event({
                    "event": "MoM Edited",
                    "timestamp": st.session_state.file_info["timestamp"],
                    "edit": "Manual Edit"
                })
                st.success("Edits saved successfully!")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<h2 class='section-title'>Download Your Minutes</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.download_button("Markdown (.md)", st.session_state.updated_summary, file_name="mom.md")
        with col2:
            st.download_button("Plaintext (.txt)", st.session_state.updated_summary, file_name="mom.txt")
        with col3:
            st.download_button("Word (.docx)", export_docx(st.session_state.updated_summary), file_name="mom.docx")
        with col4:
            st.download_button("PDF (.pdf)", export_pdf(st.session_state.updated_summary), file_name="mom.pdf", mime="application/pdf")
            
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Show Session Logs", expanded=False):
        st.markdown("<div class='main-container' style='margin-top:0;'>", unsafe_allow_html=True)
        logs = get_logs()
        st.write(logs)
        st.markdown("</div>", unsafe_allow_html=True)


else:
    st.markdown(
        """
        <div class="placeholder">
            <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" fill="var(--primary-color)" class="bi bi-file-earmark-text" viewBox="0 0 16 16">
                <path d="M5.5 7a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5zM5.5 9a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5zM5.5 11a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1h-2z"/>
                <path d="M9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.5L9.5 0zm0 1v2.5a.5.5 0 0 0 .5.5H12v9.5a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5z"/>
            </svg>
            <p class="placeholder-text">Your generated minutes will appear here.<br>Start by uploading a file above.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
