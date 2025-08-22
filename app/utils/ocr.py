import pdfplumber
import pytesseract
from PIL import Image

def extract_text_ocr(filepath:str):
    ext = filepath.lower().split('.')[-1]
    text = ""
    if ext == "pdf":
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
                # Optional: OCR for scanned pdfs
                im = page.to_image(resolution=300).original
                text += pytesseract.image_to_string(im)
    else:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
    return text
