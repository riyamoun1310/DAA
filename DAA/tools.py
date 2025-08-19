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

# General data analysis tool for uploaded CSVs
async def run_file_analysis_task(dataset_path: str, questions: str):
    df = pd.read_csv(dataset_path)
    # Placeholder: return basic info
    return {"columns": list(df.columns), "shape": df.shape}
