import os
import datetime
from io import BytesIO
import re
from docx import Document

def handle_uploaded_file(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[-1].lower()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{os.path.splitext(uploaded_file.name)[0]}_{timestamp}{ext}"
    target_dir = "./data/uploads/"
    os.makedirs(target_dir, exist_ok=True)
    filepath = os.path.join(target_dir, safe_filename)
    
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return {"filepath": filepath, "ext": ext, "timestamp": timestamp, "filename": safe_filename}

def consolidate_text(text:str):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = "./data/transcripts/"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"meeting_{timestamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

def export_docx(mom_text:str):
    doc = Document()
    for para in mom_text.split("\n"):
        doc.add_paragraph(para)
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

from fpdf import FPDF

def export_pdf(mom_text: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', '', 14)

    # Convert text to Latin-1, replacing unknown chars with '?'
    safe_text = mom_text.encode('latin-1', 'replace').decode('latin-1')

    # Helper to split huge "words" that could overflow FPDF, e.g., long URLs or unicode
    def split_long_words(line, maxlen=40):
        words = []
        for word in line.split(' '):
            if len(word) > maxlen:
                # insert zero-width space every maxlen chars (so FPDF can wrap)
                parts = [word[i:i+maxlen] for i in range(0, len(word), maxlen)]
                words.extend(parts)
            else:
                words.append(word)
        return ' '.join(words)

    # Write each line, wrapping long words as needed
    for raw_line in safe_text.splitlines():
        # Clean line endings just in case
        line = raw_line.strip()
        if not line:
            pdf.cell(0, 10, '', ln=True)
            continue
        safe_line = split_long_words(line)
        try:
            pdf.multi_cell(0, 10, safe_line)
        except Exception as e:
            # As a failsafe, chunk into smaller parts if still erroring
            for chunk in re.findall(".{1,40}", safe_line):
                pdf.cell(0, 10, chunk, ln=True)

    # Write PDF to memory file
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes