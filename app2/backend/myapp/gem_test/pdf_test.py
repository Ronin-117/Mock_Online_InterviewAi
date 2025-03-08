import PyPDF2

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

if __name__ == "__main__":
    pdf_file = r"C:\Users\njne2\Desktop\Neil Joseph.pdf"  # Replace with your file path
    text = extract_text_from_pdf(pdf_file)
    print(text)