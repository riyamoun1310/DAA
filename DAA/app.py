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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client if API key is present
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
cohere_client = None
if COHERE_API_KEY:
    cohere_client = cohere.Client(COHERE_API_KEY)
import networkx as nx
import matplotlib.pyplot as plt
import base64
from io import BytesIO

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

@app.api_route("/", response_class=HTMLResponse, methods=["GET", "HEAD"])
def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api")
async def analyze(dataset: UploadFile = File(...)):
    temp_dir = tempfile.mkdtemp()
    dataset_path = None
    log_path = os.path.join(temp_dir, "error.log")
    try:
        # Save uploaded file
        dataset_path = os.path.join(temp_dir, dataset.filename)
        with open(dataset_path, "wb") as f:
            shutil.copyfileobj(dataset.file, f)

        # Try to read as edge list (CSV with two columns: source,target)
        try:
            df = pd.read_csv(dataset_path)
            if df.shape[1] < 2:
                raise ValueError("Dataset must have at least two columns for edges.")
            G = nx.from_pandas_edgelist(df, source=df.columns[0], target=df.columns[1])
        except Exception as e:
            # If not a valid edge list, try to read as adjacency matrix
            try:
                df = pd.read_csv(dataset_path, index_col=0)
                G = nx.from_pandas_adjacency(df)
            except Exception as e2:
                raise ValueError("Dataset must be a valid edge list or adjacency matrix CSV.")

        # Calculate required metrics
        edge_count = G.number_of_edges()
        degrees = dict(G.degree())
        highest_degree_node = max(degrees, key=degrees.get) if degrees else None
        average_degree = float(np.mean(list(degrees.values()))) if degrees else 0.0
        density = nx.density(G)
        # Shortest path from 'Alice' to 'Eve' (if both exist)
        if 'Alice' in G and 'Eve' in G:
            try:
                shortest_path_alice_eve = nx.shortest_path_length(G, 'Alice', 'Eve')
            except Exception:
                shortest_path_alice_eve = None
        else:
            shortest_path_alice_eve = None

        # Draw network graph
        plt.figure(figsize=(6, 4))
        nx.draw(G, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500, font_size=8)
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        network_graph_b64 = base64.b64encode(buf.read()).decode('utf-8')

        # Degree histogram
        plt.figure(figsize=(6, 4))
        plt.hist(list(degrees.values()), bins=range(1, max(degrees.values())+2) if degrees else [1], color='orange', edgecolor='black')
        plt.xlabel('Degree')
        plt.ylabel('Count')
        plt.title('Degree Histogram')
        buf2 = BytesIO()
        plt.tight_layout()
        plt.savefig(buf2, format='png')
        plt.close()
        buf2.seek(0)
        degree_histogram_b64 = base64.b64encode(buf2.read()).decode('utf-8')

        response = {
            "edge_count": edge_count,
            "highest_degree_node": highest_degree_node,
            "average_degree": average_degree,
            "density": density,
            "shortest_path_alice_eve": shortest_path_alice_eve,
            "network_graph": network_graph_b64,
            "degree_histogram": degree_histogram_b64
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


# Add POST / endpoint after analyze is defined
@app.post("/")
async def analyze_root(dataset: UploadFile = File(...)):
    return await analyze(dataset)

@app.get("/summary")
def summary():
    return {"status": "ok", "author": "Riya Moun"}
