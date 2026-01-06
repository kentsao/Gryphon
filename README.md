# 🦁 Gryphon: AI Portfolio Manager

Gryphon is an autonomous Multi-Agent System (MAS) designed to act as your personal Investment Committee. It employs a team of specialized AI agents to research, analyze, and debate stock market moves before providing a synthesized recommendation.

> **Disclaimer**: This is a prototype (MVP) for educational purposes only. It is **NOT** financial advice.

## 🚀 Key Features

-   **Multi-Agent Architecture**: Built with [CrewAI](https://crewai.com).
    -   **The Scout**: Scours the web for news, sentiment, and earnings reports.
    -   **The Analyst**: Performs technical analysis (RSI, MACD, SMA) on price history.
    -   **The Guard**: Evaluates risk and portfolio exposure.
    -   **The Strategist**: Synthesizes all data into a final Buy/Sell/Hold verdict.
-   **Dashboard**: Interactive "War Room" UI built with [Streamlit](https://streamlit.io).
-   **Cost-Effective**: Optimized for free/low-cost LLMs (Google Gemini Flash) and free data (Yahoo Finance, DuckDuckGo).

## 🛠️ Tech Stack

-   **Language**: Python 3.12+
-   **Orchestration**: CrewAI
-   **LLM**: Google Gemini (via `langchain-google-genai`)
-   **Data**: `yfinance`, `duckduckgo-search`
-   **Analysis**: `pandas-ta`
-   **UI**: Streamlit

## 📦 Installation

1.  **Set up the Environment**:
    We recommend using Conda:
    ```bash
    conda env create -f environment.yml
    conda activate gryphon
    ```
    Or manually with pip:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Keys**:
    Create a `.env` file in the root directory:
    ```bash
    # .env
    CREWAI_TELEMETRY_OPT_OUT=true
    GOOGLE_API_KEY=your_google_api_key_here
    GOOGLE_MODEL_NAME=gemini-1.5-flash
    ```
    *Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).*

## 🚦 Usage

### 1. The Dashboard (Recommended)
Run the web interface to see the agents in action:
```bash
streamlit run app.py
```
- Enter a ticker (e.g., `NVDA`, `TSLA`, `AAPL`).
- Click **Initialize Logic**.
- Watch the **War Room** tab for live agent logs.
- View the **Verdict** tab for the final report.

### 2. The CLI
Quick scan from the terminal:
```bash
python main.py TSLA
```

## ⚠️ Known Issues
-   **"Signal only works in main thread"**: This is a known Issue with CrewAI telemetry in Streamlit. It is fixed by setting `CREWAI_TELEMETRY_OPT_OUT=true` in your `.env`.
