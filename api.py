import re
import fitz  # PyMuPDF
from fastapi import FastAPI, UploadFile, File
from fastapi.concurrency import run_in_threadpool
from transformers import pipeline
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Yes,API is running mate! Kindly visit instructions in github repo."}

# Pipelines
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
ner = pipeline("ner", grouped_entities=True)

def extract_dates_regex(text: str):
    date_patterns = [
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",   # 19/09/2025 or 19-09-2025
        r"\b(?:\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",     # 2025-09-19
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b"
    ]
    found = []
    for pattern in date_patterns:
        found.extend(re.findall(pattern, text))
    return found

async def summarize_text_async(text: str) -> str:
    
    text = " ".join(text.split())  # clean whitespace
    truncated_text = text[:1500]   # keep within model limit
    try:
        summary_list = await run_in_threadpool(
            summarizer, truncated_text, max_length=150, min_length=30, do_sample=False
        )
        return summary_list[0]['summary_text']
    except Exception as e:
        print("Summarization error:", e)
        return "AI summarization failed."

async def extract_entities_async(text: str):
    try:
        entities = await run_in_threadpool(ner, text[:1000])  # limit size
        result = {"person": [], "organization": [], "location": [], "date": []}

        label_map = {
            "PER": "person",
            "ORG": "organization",
            "LOC": "location",
            "GPE": "location",   # geopolitical entities
            #"DATE": "date"
        }

        for ent in entities:
            label = ent["entity_group"]
            word = ent["word"]

            # Map to your schema if known
            if label in label_map:
                result[label_map[label]].append(word)

        result["date"].extend(extract_dates_regex(text))

        return result
    except Exception as e:
        print("NER error:", e)
        return {"person": [], "organization": [], "location": [], "date": []}


@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    # Extract text from PDF
    request_id = request_id = datetime.now().strftime("%Y%m%d-%H_%M_%S-%f")
    doc = fitz.open(stream=await file.read(), filetype="pdf")
    text = "".join(page.get_text() for page in doc)
    text = " ".join(text.split())  # clean text

    # Run AI tasks
    summary = await summarize_text_async(text)
    entities = await extract_entities_async(text)

    return {
        "request_id": request_id,
        "filename": file.filename,
        "status": "registered",
        "summary": summary,
        "person": entities.get("person", []),
        "organization": entities.get("organization", []),
        "location": entities.get("location", []),
        "date": entities.get("date", [])
    }
