from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from ..database.ingestor import DataIngestor
from ..config.config import DATA_PATH

app = FastAPI(title="CISO Data Ingestion API")

@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = os.path.join(DATA_PATH, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ingestor = DataIngestor()
        ingestor.process_pdfs()
        
        return {"message": f"File '{file.filename}' ingested and embedded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)

@app.get("/health")
def health_check():
    return {"status": "online"}