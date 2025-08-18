# ⚡ Data Analyst Agent — Your AI-Powered Data Companion

Smarter, faster, and more intuitive analysis of your datasets using Generative AI + Python magic.

Repository: https://github.com/riyamoun1310/DAA

## 📌 What Is This?
Meet Data Analyst Agent 2.0 — an AI-driven assistant that eliminates tedious data crunching. Upload your dataset + queries, and instantly get:
- ✅ Visual reports
- ✅ AI-generated insights
- ✅ Automated workflows

Perfect for:
- Analysts 🧾
- Researchers 🔬
- Startups & Businesses 📈
- Anyone who loves turning raw data into knowledge

## ✨ Key Highlights
- 🤖 AI-Powered Insights: Uses Google’s Generative AI to “understand” your data
- 📊 Rich Visualizations: Generates plots with Seaborn & Matplotlib
- 🌍 Web Scraper Mode: Fetch live data directly from URLs
- 📂 Multi-Format Friendly: Accepts CSV, Excel, JSON, Parquet, or TXT
- 🔄 Ask Many at Once: Batch processing for multiple questions
- 🖥️ Simple-to-Use Interface: Beginner friendly, no steep learning curve
- ⚡ Super-Fast Execution: Optimized for speed + real-time feedback

## 🚀 Getting Started
1. Clone the Repo
```sh
git clone https://github.com/riyamoun1310/DAA.git
cd DAA
```
2. Install Requirements
```sh
pip install -r requirements.txt
```
3. Configure API Keys
Create a `.env` file inside the root folder:
```
GEMINI_API_KEY=your_google_api_key
LLM_TIMEOUT_SECONDS=240
```
4. Start the Application
```sh
python -m uvicorn app:app --reload
```
Now open [http://localhost:8000/](http://localhost:8000/) in your browser 🌐

## 🧑‍💻 How It Works
1. Write Your Questions: Create a `.txt` file with queries like: What’s the revenue growth month-over-month? Find correlation between Age and Income, Show most profitable products, etc.
2. Upload Dataset + Questions File
   - Dataset (optional): CSV, Excel, JSON, Parquet, or TXT
   - Questions file (required): Plain text
3. Voilà!
   - AI processes the queries
   - Generates insights + summaries
   - Builds neat visualizations

## 🛠 Tech Behind the Scenes
### Backend
- FastAPI ⚡
- LangChain 🧠
- Google Generative AI ✨
- Pandas + NumPy 📊
- Seaborn + Matplotlib 🎨

### Frontend
- HTML5 + CSS + JavaScript
- Bootstrap-inspired modern UI

## 🔧 API Blueprint
- GET / : Access web app
- POST /api : Submit dataset + questions
- GET /summary : App diagnostics & summaries

## 📂 File Support
- CSV (.csv)
- Excel (.xlsx, .xls)
- JSON (.json)
- Parquet (.parquet)
- Text (.txt)

## 🎯 Where Can You Use This?
- 📈 Business Strategy – Sales, KPIs, forecasts
- 🔬 Research – Data exploration, hypothesis validation
- 🤖 Data Science – Quick EDA, anomaly detection
- 📊 Reporting – Automated dashboards

## 🔒 Security First
- No cloud storage → All data stays local
- API keys kept safe via `.env`
- Configurable CORS policy for production use

## 📜 License
MIT License — free for personal & commercial use.

---
© 2025 Riya Moun
