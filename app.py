import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import tempfile
import shutil
import cohere

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
    temp_dir = tempfile.mkdtemp()
    dataset_path = None
    log_path = os.path.join(temp_dir, "error.log")
    try:
        if dataset:
            dataset_path = os.path.join(temp_dir, dataset.filename)
            with open(dataset_path, "wb") as f:
                shutil.copyfileobj(dataset.file, f)
        questions_path = os.path.join(temp_dir, questions.filename)
        with open(questions_path, "wb") as f:
            shutil.copyfileobj(questions.file, f)
        # Read questions from file
        with open(questions_path, "r", encoding="utf-8") as f:
            questions_list = [q.strip() for q in f.readlines() if q.strip()]

        # Use OpenAI API to answer each question
        co = cohere.Client("D7Yn2rfXryO4zZ33XlWSNhojSEgoUA16F8UIByup")
        insights = []
        for q in questions_list:
            try:
                response = co.generate(
                    model="command-r-plus",
                    prompt=q,
                    max_tokens=256
                )
                insights.append(response.generations[0].text.strip())
            except Exception as e:
                insights.append(f"Cohere API error: {str(e)}")

        response = {
            "author": "Riya Moun",
            "dataset": dataset.filename if dataset else None,
            "questions": questions.filename,
            "insights": insights
        }
        shutil.rmtree(temp_dir)
        return JSONResponse(content=response)
    except Exception as e:
        # Log error to file
        with open(log_path, "w", encoding="utf-8") as logf:
            import traceback
            logf.write(traceback.format_exc())
        shutil.rmtree(temp_dir)
        return JSONResponse(status_code=500, content={"error": str(e), "details": f"See {log_path}"})

@app.get("/summary")
def summary():
    return {"status": "ok", "author": "Riya Moun"}
