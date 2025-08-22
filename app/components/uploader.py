import streamlit as st

def file_uploader_component():
    st.markdown("**Step 1:** Upload Audio, Transcript, PDF, or Image")

    uploaded_file = st.file_uploader(
        label="Upload file (.mp3, .wav, .txt, .pdf, .jpg, .png)",
        type=["mp3", "wav", "txt", "pdf", "jpg", "jpeg", "png"]
    )

    # Participant tagging
    st.markdown("**Step 2 (Optional):** Tag participants")
    participant_tag = st.multiselect("Known Participants:", 
        options=["Alice", "Bob", "Claim Manager", "Medical Officer", "External Auditor"])
    manual_participant_entry = st.text_input("Manual entry (comma separated):")

    return uploaded_file, participant_tag, manual_participant_entry
