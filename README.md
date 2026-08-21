# ⚡ SkillRadar: AI-Powered Tech Job Market Intelligence

SkillRadar is an automated data pipeline and analytics dashboard that tracks in-demand tech skills, compensation trends, and remote developer roles using **Bright Data Scraper Studio**.

## 🚀 Key Features
- **Scraper Studio Integration:** Cloud-hosted AI collector extracting structured job listings directly into Python.
- **Self-Healing Web Scraping:** Handles website structure and DOM changes via `bdata scraper heal` without breaking the downstream data pipeline.
- **Data Analytics Engine:** Automatic deduplication, salary normalization, and regex-based tech skill frequency analysis.
- **Interactive UI:** Built with Streamlit and Plotly featuring real-time KPI metrics, search filtering, and pipeline health monitoring.

## 🛠️ Tech Stack
- **Data Ingestion:** Bright Data Scraper Studio (`bdata` CLI & REST API)
- **Processing & Analytics:** Python, Pandas, Regex
- **Dashboard:** Streamlit, Plotly
- **Environment:** `python-dotenv`

## ⚙️ Installation & Setup

```bash
git clone https://github.com/Avani2506/skill-radar.git
cd skill-radar
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
BRIGHT_DATA_API_TOKEN=your_bright_data_api_token
COLLECTOR_ID=your_scraper_studio_collector_id
```

These credentials power live data collection via the Bright Data Scraper Studio API. Without them, the dashboard falls back to `data/sample_output.json` or built-in mock data.

## ▶️ Running the Dashboard

```bash
streamlit run src/dashboard/app.py
```

The app opens in your browser with three tabs:

1. **Market Analytics** — Top skills, salary distribution, and KPI metrics
2. **Job Explorer** — Search and filter remote job postings
3. **Pipeline & Self-Healing Health** — Collector status and healing commands

## 🔄 Self-Healing Scraper

If the target site changes its layout and field extraction drifts, trigger a self-healing routine from the CLI:

```powershell
bdata scraper heal <COLLECTOR_ID> "Fix extraction for updated page layout"
```

Replace `<COLLECTOR_ID>` with the value from your `.env` file.

## 📁 Project Structure

```
skill-radar/
├── src/
│   ├── scraper/
│   │   └── collector_client.py   # Bright Data API client
│   ├── processor/
│   │   ├── cleaner.py            # Deduplication & salary parsing
│   │   └── skill_analyzer.py     # Skill extraction & market metrics
│   └── dashboard/
│       └── app.py                # Streamlit dashboard
├── data/
│   └── sample_output.json        # Fallback sample dataset
├── tests/
│   └── test_processor.py         # Processor pipeline test
├── requirements.txt
└── .env                          # API credentials (not committed)
```

## 🧪 Running Tests

```bash
python tests/test_processor.py
```

## 📊 Data Pipeline

```
We Work Remotely (target URL)
        ↓
Bright Data Scraper Studio (collector trigger + poll)
        ↓
DataCleaner (dedupe, salary normalize, remote flags)
        ↓
SkillAnalyzer (skill frequency, market metrics)
        ↓
Streamlit Dashboard (charts, search, health monitor)
```

Default scrape target: `https://weworkremotely.com/categories/remote-programming-jobs`
