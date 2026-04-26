# import FastAPI tools
from fastapi import FastAPI, UploadFile, File

# import PDF reader
import PyPDF2

# create the app
app = FastAPI()

# homepage route
@app.get("/")
def home():
    return {"message": "AI Resume Screener is running"}

# route for uploading a resume PDF
@app.post("/upload")
def upload_resume(file: UploadFile = File(...)):

    # read the uploaded PDF
    pdf_reader = PyPDF2.PdfReader(file.file)

    resume_text = ""

    # extract text from each page
    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            resume_text += page_text + "\n"

    # return only the first part for testing
    return {"resume_text": resume_text[:500]}