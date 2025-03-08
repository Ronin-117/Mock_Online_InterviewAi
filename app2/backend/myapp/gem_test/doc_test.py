from docx import Document

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

if __name__ == "__main__":
    docx_file = r"C:\Users\njne2\Desktop\Neil Joseph.docx"  # Replace with your file path
    text = extract_text_from_docx(docx_file)
    print(text)