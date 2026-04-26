from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.database import csv_to_sql
from app.vector_store import process_pdf
from app.agent import ask_datapilot
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "DataPilot API is running!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    if file.filename.endswith(".csv"):
        table_name = file.filename.replace(".csv", "").lower()
        csv_to_sql(file_path, table_name)
        return {"message": f"CSV '{file.filename}' processed into table '{table_name}'"}
    
    elif file.filename.endswith(".pdf"):
        num_chunks = process_pdf(file_path)
        return {"message": f"PDF '{file.filename}' processed into {num_chunks} vector chunks"}
    
    return {"error": "Unsupported file format. Please upload CSV or PDF."}

@app.post("/chat")
async def chat(message: str = Form(...)):
    try:
        response = ask_datapilot(message)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
