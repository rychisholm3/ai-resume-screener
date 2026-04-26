import PyPDF2


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file.file)

    resume_text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            resume_text += page_text + "\n"

    return resume_text