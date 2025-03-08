import PyPDF2
from docx import Document


def extract_text_from_pdf(filepath):
    """Extracts text from a PDF file and returns it as a string."""
    try:
        pdf_file = open(filepath, 'rb')  # Open in binary mode for PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        full_text = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            full_text.append(page.extract_text())
        pdf_file.close()
        return "\n".join(full_text)
    except Exception as e:
        return f"Error processing PDF file: {e}"
    
def extract_text_from_docx(filepath):
    """Extracts text from a DOCX file and returns it as a string."""
    try:
        doc = Document(filepath)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        return f"Error processing DOCX file: {e}"

def get_resume(resume_path):
    if resume_path.endswith(".pdf"):
        text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith(".docx"):
        text = extract_text_from_docx(resume_path)
    else:
        text = "content for the resume is not provided or the file format is not supported" 
    return text

if __name__ == "__main__":
    resume_file = r"C:\Users\njne2\Desktop\Neil Joseph.pdf"  # Replace with your file path
    resume_text = get_resume(resume_file)
    print(resume_text)