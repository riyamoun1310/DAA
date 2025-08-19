import os
import tempfile
import shutil
from typing import List

import cohere
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import your tool functions
from data_analyst_agent.duckdb_tool import run_duckdb_query
from data_analyst_agent.tools import run_file_analysis_task, run_scraping_task

# Load environment variables ONCE from .env file
load_dotenv()

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None


# Initialize FastAPI app
app = FastAPI(title="Data Analyst Agent — Riya Moun")

# --- Global Exception Handlers for JSON errors ---
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors()},
    )

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Agent/Router Logic ---
async def process_task(questions_file: UploadFile, other_files: List[UploadFile]):
    """
    This is the core agent that reads the user's question and routes it to the correct tool.
    """
    questions_content = (await questions_file.read()).decode('utf-8')

    # Helper function to wrap the output in the correct JSON format (array or object)
    def wrap_output(result, questions):
        if "array" in questions.lower():
            return result if isinstance(result, list) else [result]
        else:
            return result if isinstance(result, dict) else {"result": result}

    # --- Tool Selection Logic ---

    # 1. DuckDB/SQL task detection
    if "high court judgement" in questions_content.lower() or "duckdb" in questions_content.lower():
        # This task might not need a separate file, but the structure is here if needed
        if other_files:
            temp_dir = tempfile.mkdtemp()
            dataset_path = os.path.join(temp_dir, other_files[0].filename)
            with open(dataset_path, "wb") as f:
                shutil.copyfileobj(other_files[0].file, f)
            result = run_duckdb_query(dataset_path, questions_content)
            shutil.rmtree(temp_dir)
            return wrap_output(result, questions_content)
        else:
            # Handle DuckDB queries that don't require file uploads
            result = run_duckdb_query(None, questions_content)
            return wrap_output(result, questions_content)

    # 2. Web scraping task detection
    elif "scrape" in questions_content.lower() and "wikipedia" in questions_content.lower():
        url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
        result = await run_scraping_task(url, questions_content)
        return wrap_output(result, questions_content)

    # 3. General file analysis with LLM (if other files are provided)
    elif other_files:
        temp_dir = tempfile.mkdtemp()
        dataset_path = os.path.join(temp_dir, other_files[0].filename)
        with open(dataset_path, "wb") as f:
            shutil.copyfileobj(other_files[0].file, f)
        
        # Pass the initialized cohere_client to the tool
        result = await run_file_analysis_task(dataset_path, questions_content, cohere_client)
        shutil.rmtree(temp_dir)
        return wrap_output(result, questions_content)

    # 4. Fallback if no specific tool is matched
    else:
        return {"error": "Could not determine the task type or no data file was provided for analysis."}


# --- API Endpoints ---

@app.api_route("/", response_class=HTMLResponse, methods=["GET", "HEAD"])
def root():
    """Serves the main HTML page."""
    # Construct an absolute path to index.html to avoid path issues
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>index.html not found</h1>"



# Flexible /api endpoint: accept both 'questions_txt' and 'questions' as field names
@app.post("/api", response_class=JSONResponse)
async def handle_analysis_request(
    questions_txt: UploadFile = File(None),
    questions: UploadFile = File(None),
    files: List[UploadFile] = File(None)
):
    """
    The main API endpoint that receives the user's question and data files.
    """
    try:
        # Log incoming field names for debugging
        import logging
        logging.basicConfig(level=logging.INFO)
        field_info = {
            'questions_txt': bool(questions_txt),
            'questions': bool(questions),
            'files_count': len(files) if files else 0,
            'files_names': [f.filename for f in files] if files else []
        }
        logging.info(f"Incoming fields: {field_info}")

        # Accept either field name for the questions file
        questions_file = questions_txt or questions
        data_files = []

        # If neither is present, but files is present
        if not questions_file and files and len(files) > 0:
            # Try to find a .txt file in files
            txt_files = [f for f in files if f.filename.lower().endswith('.txt')]
            if txt_files:
                questions_file = txt_files[0]
                data_files = [f for f in files if f != questions_file]
            else:
                # Fallback: use first file as questions_file
                questions_file = files[0]
                data_files = files[1:] if len(files) > 1 else []
        else:
            # Filter out the questions.txt file from the list of data files
            data_files = [f for f in files if f.filename != 'questions.txt'] if files else []

        if not questions_file:
            return JSONResponse(status_code=422, content={"error": "Missing questions file."})

        response = await process_task(questions_file, data_files)
        return JSONResponse(content=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})


@app.get("/summary")
def summary():
    """A simple endpoint for health checks and diagnostics."""
    return {"status": "ok", "author": "Riya Moun"}