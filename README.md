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
    GOOGLE_MODEL_NAME=gemini-2.5-flash-lite
    ```
    *Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).*

## 🚀 Usage

1.  **Start the App**:
    ```bash
    streamlit run app.py
    ```

2.  **Authentication**:
    -   You will be greeted by a Login screen.
    -   Switch to the **Register** tab to create a secure account (managed by Supabase).

3.  **Portfolio Manager** (New!):
    -   Navigate to "Portfolio Manager" in the sidebar.
    -   **Create Portfolio**: detailed collections of your assets.
    -   **Add Holdings**: Input tickers and shares.
    -   **Risk Engine**: Click "Calculate Risk Metrics" to see Beta, Sharpe Ratio, and Volatility key stats.
    -   **AI Advisor**: Select your Risk Profile and ask the AI for a **Rebalancing Plan** (includes new asset suggestions!).

4.  **Generation Engine** (Original):
    -   Switch to "Generation Engine" to run deep-dive agents on specific stock tickers (News + Fundamentals + Technicals).

5.  **Admin Console**:
    -   Access system stats at the `admin_dashboard` page (via sidebar).

### 2. The CLI
Quick scan from the terminal:
```bash
python main.py TSLA
```

## 📊 Quantitative Methodology

Gryphon's **Risk Engine** calculates key metrics to assess portfolio health, using `SPY` (S&P 500) as the benchmark.

1.  **Beta ($\beta$)**: Measures volatility relative to the market.
    *   *Calculation*: `Covariance(Portfolio, Market) / Variance(Market)`
    *   *Why*: $\beta > 1$ means high exposure (aggressive); $\beta < 1$ means lower volatility (defensive).
2.  **Volatility ($\sigma$)**: Annualized standard deviation of daily returns.
    *   *Calculation*: `StdDev(Daily Returns) * sqrt(252)`
    *   *Why*: Represents the range of price fluctuations. High $\sigma$ = higher risk.
3.  **Sharpe Ratio**: Risk-adjusted return.
    *   *Calculation*: `(Portfolio Return - Risk Free Rate) / Volatility`
    *   *Why*: Tells you if the returns are worth the risk. A ratio $> 1$ is generally considered good.
4.  **Max Drawdown**: The largest peak-to-trough decline.
    *   *Calculation*: `Min((Current Value - Peak Value) / Peak Value)`
    *   *Why*: Stress-tests the portfolio's "worst-case scenario" based on historical data.

## ⚠️ Known Issues
-   **"Signal only works in main thread"**: This is a known Issue with CrewAI telemetry in Streamlit. It is fixed by setting `CREWAI_TELEMETRY_OPT_OUT=true` in your `.env`.
