import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import tempfile
import shutil

# Load environment variables
load_dotenv()

app = FastAPI(title="Data Analyst Agent — Riya Moun")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api")
async def analyze(dataset: UploadFile = File(None), questions: UploadFile = File(...)):
    # Save uploaded files to temp
    temp_dir = tempfile.mkdtemp()
    dataset_path = None
    if dataset:
        dataset_path = os.path.join(temp_dir, dataset.filename)
        with open(dataset_path, "wb") as f:
            shutil.copyfileobj(dataset.file, f)
    questions_path = os.path.join(temp_dir, questions.filename)
    with open(questions_path, "wb") as f:
        shutil.copyfileobj(questions.file, f)
    # Dummy response (replace with AI logic)
    response = {
        "author": "Riya Moun",
        "dataset": dataset.filename if dataset else None,
        "questions": questions.filename,
        "insights": [
            "This is a personalized Data Analyst Agent for Riya Moun.",
            "Replace this with actual AI-powered insights!"
        ]
    }
    shutil.rmtree(temp_dir)
    return JSONResponse(content=response)

@app.get("/summary")
def summary():
    return {"status": "ok", "author": "Riya Moun"}
