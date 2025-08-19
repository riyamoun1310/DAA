import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import tempfile
import os
import shutil

# Web scraping tool for Wikipedia tables
async def run_scraping_task(url: str, questions: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    df = pd.read_html(str(table))[0]
    # Placeholder: return the first 5 rows as JSON
    return {"table_head": df.head().to_dict()}


# General data analysis tool for uploaded CSVs using LLM
import cohere
import traceback
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import json
import os

def safe_exec(code: str, local_vars: dict):
    try:
        exec(code, {}, local_vars)
        return local_vars
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

async def run_file_analysis_task(dataset_path: str, questions: str):
    df = pd.read_csv(dataset_path)
    # Get Cohere API key from env
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    if not COHERE_API_KEY:
        return {"error": "Cohere API key not found."}
    co = cohere.Client(COHERE_API_KEY)
    # Prompt LLM to generate code
    prompt = f"""
You are a Python data analyst. Given a pandas DataFrame `df` with columns: {list(df.columns)}, answer the following question(s):\n{questions}\nWrite Python code to compute the answer. If a plot is required, save it to a BytesIO buffer as PNG and base64 encode it as 'plot_b64'. Return all answers in a dict called 'result'.\nExample:\nresult = {'answer': ..., 'plot_b64': ...}
"""
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=512,
        temperature=0.2
    )
    code = response.generations[0].text.strip()
    # Prepare local vars for exec
    local_vars = {"df": df, "plt": plt, "BytesIO": BytesIO, "base64": base64, "result": {}}
    exec_result = safe_exec(code, local_vars)
    if "error" in exec_result:
        return {"error": "LLM code execution failed", "details": exec_result["error"], "traceback": exec_result.get("traceback","")}
    result = local_vars.get("result", {})
    # If plot_b64 is present, ensure it's under 100,000 bytes
    if "plot_b64" in result:
        if len(result["plot_b64"]) > 100000:
            result["plot_b64"] = result["plot_b64"][:100000]
    return result
