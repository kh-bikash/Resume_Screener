import io
from PyPDF2 import PdfReader

def extract_text(uploaded_file):
    """Extracts text from a Streamlit UploadedFile object."""
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text
    else:
        # Assume it's a text file
        return uploaded_file.read().decode("utf-8", errors="ignore")
