# Final Capstone Project Report
## AI Engineering on Cloud and AIOps Certification
**Joint Certification by IIT Roorkee and Futurense**

---

# 1. Cover Page

* **Project Title:** AI Investment Research Assistant: Autonomous Multi-Agent Equity Research & Human-in-the-Loop Governance
* **Domain:** Finance
* **Theme Selected:** Theme 15 — AI Investment Research Assistant
* **Program:** Advanced PG Certification in AI Engineering on Cloud and AIOps
* **Institution:** Indian Institute of Technology (IIT) Roorkee, powered by Futurense
* **Team Members:**
  1. **Ganesh Swami** — Backend Architecture & Cloud DevOps Lead
  2. **Shradha Gaikwad** — Financial Agent Intelligence & Quantitative Modeling Lead
  3. **Sagar Trimukhe** — Frontend Dashboard & Chatbot/HITL Integration Lead
  4. **Nilanjan Das** — Data Engineering, SEC Filings & Vector RAG Pipeline Lead
  5. **Nikhil Gaikwad** — Full-Stack Integration, Telemetry & Quality Assurance Lead
* **Submission Module:** Module 15 — Capstone Project Submission
* **Cohort Duration:** 08 September 2026 – 09 October 2026
* **Submission Date:** 09 October 2026

---

# 2. Executive Summary

Equity research analysts at institutional investment firms, hedge funds, and wealth management desks face an escalating challenge: analyzing 100+ page SEC Form 10-K and 10-Q filings, synthesizing market sentiment across earnings transcripts, calculating real-time peer valuation multiples, and drafting rigorous investment memorandums within hours of earnings releases. Manual execution of this workflow is error-prone, cognitively exhausting, and unscalable.

To solve this, our team developed the **AI Investment Research Assistant**, an enterprise-grade, multi-agent AI system built using **LangGraph**, **ChromaDB**, **LangChain**, and **Google Gemini LLMs**, deployed on **AWS (EC2 & S3)**. 

The system implements a stateful Directed Acyclic Graph (DAG) with **parallel fan-out execution**:
1. An intelligent **Router Node** validates input tickers and pairs them with benchmark industry competitors.
2. A **Market Research Agent** queries a ChromaDB vector store via ticker-filtered RAG to extract balance sheet fundamentals, gross profits, and risk factors from 10-K filings.
3. Concurrently, a **Trend & Sentiment Analysis Agent** evaluates macroeconomic tailwinds and assigns quantitative sentiment scores.
4. A **Comparative Valuation Agent** uses real-time `yfinance` telemetry to benchmark Trailing/Forward P/E, EV/EBITDA, and market capitalization against peer competitors.
5. A **Summary Agent** synthesizes qualitative findings with mathematical risk engines (calculating **252-day annualized historical volatility** and **rolling maximum drawdown**) to produce a structured investment thesis and 12-month target price.
6. A **Human-in-the-Loop (HITL) Review Gate** freezes workflow execution before final publication, giving human analysts full audit authority to adjust target prices, add notes, and sign off.
7. Upon approval, memorandums are exported as publication-ready Markdown reports and archived directly to **AWS S3**.

The final application is containerized with Docker, deployed on an **AWS EC2 `t3.medium`** instance, and features an offline stock universe of **270 NASDAQ companies** alongside **20 genuine official SEC EDGAR 10-K filings**.

---

# 3. Problem Statement

Financial market decisions require high-conviction, verifiable analysis synthesized from three distinct sources of information:
1. **Unstructured Historical Disclosures:** SEC annual reports (Form 10-K) contain 50–200 pages of dense accounting notes, operational risk factors, and debt schedules.
2. **Dynamic Macroeconomic & Industry Drivers:** Sector trends, interest rate environments, and consumer demand shifts that shape forward-looking revenue potential.
3. **Real-Time Market Pricing:** Live stock prices, comparative multiples (P/E, Forward P/E, PEG, EV/EBITDA), and mathematical volatility metrics relative to industry peers.

### Core Bottlenecks:
* **Context Window Overload:** Standard LLM chat interfaces cannot ingest entire 200-page filings without hallucinations, loss of numerical precision, or context window truncation.
* **Lack of Multi-Disciplinary Reasoning:** A single prompt cannot reliably extract audited numbers, analyze macro headwinds, pull live stock market APIs, and calculate mathematical volatility simultaneously.
* **Compliance & Hallucination Risks:** Financial recommendations require audited traceability. Generative AI without validation schemas or human sign-off gates cannot be trusted for institutional capital allocation.

---

# 4. Project Objectives

1. **Autonomous Multi-Agent Workflow:** Build a stateful, modular agent architecture using LangGraph that breaks down equity analysis into specialized, parallelized tasks.
2. **High-Precision RAG Ingestion Pipeline:** Implement document parsing, recursive text chunking (1500 chars / 150 overlap), high-dimensional Gemini embeddings, and ChromaDB vector storage with metadata filtering.
3. **Live Market Telemetry & Quantitative Modeling:** Integrate dynamic market data tools via `yfinance` and implement stock risk metrics (1-year price volatility across 252 trading days and historical maximum price drop).
4. **Institutional Human Governance (HITL):** Enforce human-in-the-loop review via `langgraph.types.interrupt` to ensure no investment memorandum is published without analyst sign-off.
5. **Production Cloud Deployment on AWS:** Deploy the application on AWS EC2 with automated provisioning scripts, containerize with Docker, and integrate AWS S3 for document archiving.
6. **Extensive Coverage & Verification:** Support a 270-stock universe catalog and demonstrate zero-hallucination RAG on official SEC EDGAR filings (e.g., Apple, Microsoft, NVIDIA, Amazon, Alphabet).

---

# 5. Dataset and Document Creation

To test both offline development scenarios and institutional production workloads, our team curated a dual-tier dataset architecture:

### 5.1 Genuine Official SEC EDGAR 10-K Filings
Led by **Nilanjan Das**, we built an automated SEC EDGAR downloader ([`scripts/fetch_real_10k_filings.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/scripts/fetch_real_10k_filings.py)) that interfaces with official SEC submissions APIs (`https://data.sec.gov/submissions/`) to fetch genuine, publicly filed Form 10-K documents:
* **20 Official Filings Downloaded:** Apple Inc. (`AAPL`), Microsoft (`MSFT`), NVIDIA (`NVDA`), Amazon (`AMZN`), Alphabet (`GOOGL`), Meta (`META`), Tesla (`TSLA`), Netflix (`NFLX`), AMD (`AMD`), Intel (`INTC`), Salesforce (`CRM`), Adobe (`ADBE`), PayPal (`PYPL`), Cisco (`CSCO`), Amgen (`AMGN`), Costco (`COST`), PepsiCo (`PEP`), Qualcomm (`QCOM`), Gilead (`GILD`), and Starbucks (`SBUX`).
* Each filing contains 200,000 to 640,000 characters of audited text, Item 1 (Business), Item 1A (Risk Factors), and Item 8 (Financial Statements).
* Tracked via a verified manifest: [`data/nasdaq_reports/REAL_FILINGS_MANIFEST.json`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/data/nasdaq_reports/REAL_FILINGS_MANIFEST.json).

### 5.2 Standardized NASDAQ Universe Dataset
* **270-Stock Catalog:** Implemented in [`app/services/nasdaq_universe.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/services/nasdaq_universe.py) covering Mega-Cap Tech, Semiconductors, Cloud/SaaS, Healthcare, E-Commerce, and Fintech.
* **XBRL Financial Dataset:** Standardized reports generated from official SEC EDGAR XBRL APIs (`data.sec.gov/api/xbrl/companyfacts/`) storing verified revenue, operating income, gross profit, and research & development expenses.
* **Corporate Presentations & Fact-Sheets:** Included multi-page PDFs (e.g., `Meta Earnings-Presentation-Q2-2026.pdf`, `Infosys fact-sheet.pdf`, `NVIDIA_3_Quarter_Report_Calendar_2026.pdf`) to validate multi-format PDF ingestion.

---

# 6. System Architecture

The architecture follows a layered, decoupled system design:

```
+----------------------------------------------------------------------------------------------------+
|                                    USER / ANALYST INTERACTION                                     |
|                                Streamlit Dashboard (Port 8501)                                     |
|              [Tab 1: Document Ingestion]  [Tab 2: Research & Analysis]  [Tab 3: HITL Review]       |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+----------------------------------------------------------------------------------------------------+
|                                   LANGGRAPH ORCHESTRATION ENGINE                                   |
|                                                                                                    |
|                                         ┌──────────────┐                                           |
|                                         │ Router Node  │                                           |
|                                         └──────┬───────┘                                           |
|                                                │                                                   |
|                         ┌──────────────────────┴──────────────────────┐                            |
|                         ▼ (Parallel Fan-Out)                          ▼ (Parallel Fan-Out)         |
|              ┌─────────────────────┐                       ┌─────────────────────┐                 |
|              │   Market Research   │                       │  Trend & Sentiment  │                 |
|              │   Agent (RAG)       │                       │     Analysis Agent  │                 |
|              └──────────┬──────────┘                       └──────────┬──────────┘                 |
|                         │                                             │                            |
|                         └──────────────────────┬──────────────────────┘                            |
|                                                ▼ (Fan-In State Reducer)                            |
|                                     ┌─────────────────────┐                                        |
|                                     │Comparative Valuation│ ◄──── [yfinance Telemetry Engine]      |
|                                     │       Agent         │                                        |
|                                     └──────────┬──────────┘                                        |
|                                                ▼                                                   |
|                                     ┌─────────────────────┐                                        |
|                                     │    Summary Agent    │ ◄──── [252-Day Volatility Engine]      |
|                                     └──────────┬──────────┘                                        |
|                                                ▼                                                   |
|                                     ┌─────────────────────┐                                        |
|                                     │  HITL Review Gate   │ ◄──── [Human Analyst Sign-off]         |
|                                     └──────────┬──────────┘                                        |
|                                                ▼                                                   |
|                                             [ END ]                                                |
+----------------------------------------------------------------------------------------------------+
          │                                                                           │
          ▼                                                                           ▼
+-----------------------------------+                       +----------------------------------------+
|          DATA & RAG LAYER         |                       |          AWS CLOUD INFRASTRUCTURE      |
|  - pypdf & Text Extraction        |                       |  - AWS EC2 (t3.medium, Ubuntu 22.04)   |
|  - Recursive Splitter (1500/150)  |                       |  - Docker & Docker Compose             |
|  - Gemini Embeddings (3072 Dims)  |                       |  - AWS S3: s3://ai-investment-research/ |
|  - ChromaDB Vector Store          |                       |    ├── filings/<TICKER>/ (Raw Inputs)  |
|  - Rate-Limit Exponential Backoff |                       |    └── reports/<TICKER>/ (Final Memos) |
+-----------------------------------+                       +----------------------------------------+
```

---

# 7. Agent Workflow Design

The multi-agent workflow is constructed as a compiled LangGraph state graph ([`app/services/workflow_service.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/services/workflow_service.py)) with 6 specialized nodes:

### 1. Router Node (`app/agents/router.py`) — *Shradha Gaikwad & Ganesh Swami*
* **Role:** Sanitizes inputs, validates ticker format, and assigns appropriate benchmark peers (e.g., `AAPL` -> `MSFT`; `NVDA` -> `AMD`; `TSLA` -> `F`).
* **Design Rationale:** Prevents invalid inputs from triggering costly downstream LLM queries.

### 2. Market Research Agent (`app/agents/market_research.py`) — *Shradha Gaikwad*
* **Role:** Acts as the fundamental accounting auditor.
* **Execution:** Queries ChromaDB for the target ticker's financial statements, extracting audited revenues, net income, gross margin, and top 5 risk factors.
* **Schema Validation:** Enforces strict Pydantic parsing via `FinancialMetricsReport`.

### 3. Trend & Sentiment Analysis Agent (`app/agents/trend_analysis.py`) — *Shradha Gaikwad*
* **Role:** Macroeconomic strategist.
* **Execution:** Evaluates macroeconomic backdrop, sector headwinds (supply chains, interest rates), and generates a normalized market sentiment score from -1.0 (bearish) to +1.0 (bullish).

### 4. Comparative Valuation Agent (`app/agents/comparative_analysis.py`) — *Nikhil Gaikwad & Shradha Gaikwad*
* **Role:** Valuation multiples analyst.
* **Execution:** Uses live financial tools to fetch Trailing P/E, Forward P/E, Market Cap, EV/EBITDA, and 52-week ranges for both target and benchmark companies.
* **Resilience:** Implements a dual strategy: attempts function-calling tools first, and automatically falls back to direct API calls if tool generation fails.

### 5. Summary Agent (`app/agents/summary_agent.py`) — *Shradha Gaikwad & Ganesh Swami*
* **Role:** Chief Investment Officer (CIO) synthesis.
* **Execution:** Synthesizes fundamental extraction, sentiment score, and peer valuation multiples. Computes 252-day annualized volatility and max drawdown. Formulates 12-month target price, rating recommendation (BUY / HOLD / SELL), and key catalysts.

### 6. Human-in-the-Loop Review Gate (`app/agents/hitl_review.py`) — *Ganesh Swami & Sagar Trimukhe*
* **Role:** Governance and compliance officer.
* **Execution:** Halts the graph execution using `langgraph.types.interrupt()`, yielding control to the analyst dashboard for human verification.

---

# 8. RAG Pipeline (Retrieval-Augmented Generation)

Financial filings require a zero-tolerance approach to hallucinations. Developed collaboratively by **Nilanjan Das** and **Nikhil Gaikwad**, our RAG pipeline ([`app/services/document_ingestion.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/services/document_ingestion.py)) operates through five distinct stages:

```
[Raw Filing PDF / TXT] 
        │
        ▼ 
[Text Extraction & Sanitization] (pypdf / UTF-8 zero-byte cleaner)
        │
        ▼
[Recursive Character Splitting] (Chunk Size: 1,500 chars | Overlap: 150 chars)
        │
        ▼
[Vector Embedding Engine] (Google Gemini Embedding-001 | 3,072 Dimensions)
        │
        ▼
[Persistent Vector Store] (ChromaDB with metadata: {"ticker", "source", "chunk_id"})
        │
        ▼
[Targeted Semantic Retrieval] (Vector Similarity Search filtered strictly by ticker)
```

### Key RAG Engineering Highlights:
* **Chunking Geometry:** Evaluated 500, 1000, and 1500 characters. 1,500 characters with 10% overlap (150 chars) was selected because financial 10-K tables and complex risk disclosures require complete accounting paragraphs to preserve tabular integrity.
* **Metadata Ticker Isolation:** Every chunk stored in ChromaDB contains a `ticker` metadata tag. When researching Apple, vector queries strictly filter `filter={"ticker": "AAPL"}`. This guarantees that Apple's analysis never inadvertently retrieves numbers from Microsoft or NVIDIA filings.

---

# 9. Human Approval Step (Human-in-the-Loop)

In high-stakes investment management, fully autonomous AI execution creates unacceptable regulatory and financial risks. Implemented by **Ganesh Swami** and integrated into the frontend by **Sagar Trimukhe**, we built a native **Human-in-the-Loop (HITL)** governance gate:

1. **State Interruption:** Inside `app/agents/hitl_review.py`, after the Summary Agent creates a draft thesis, the node calls:
   ```python
   human_review_payload = interrupt({
       "action": "analyst_review_required",
       "draft_recommendation": state.get("recommendation"),
       "target_price": state.get("target_price"),
       "investment_thesis": state.get("investment_thesis"),
   })
   ```
2. **Session Freezing:** LangGraph serializes the current execution state into its `MemorySaver` checkpointer and suspends the thread.
3. **Analyst Review Interface:** In Tab 3 of the Streamlit dashboard, the draft thesis is presented. The human analyst can:
   * Agree and certify the AI's recommendation.
   * Override the recommendation (e.g., change `BUY` to `HOLD`).
   * Adjust the 12-month target price.
   * Add required audit commentary.
4. **Resumption:** When the analyst clicks **"Certify and Publish Memorandum"**, the application sends `Command(resume=review_data)`, unfreezing the graph to produce the final certified memorandum.

---

# 10. Memory and Context Handling

The application manages memory and state at multiple tiers:
* **Workflow State Memory (`AgentState`):** Uses LangGraph's strongly typed state dictionary defined in `app/core/state.py`. Node inputs and outputs are deterministically tracked through the graph lifecycle.
* **Parallel State Merging via Custom Reducers:** To enable Market Research and Trend Analysis to run concurrently without corrupting shared state keys, **Ganesh Swami** implemented custom LangGraph reducers:
  ```python
  def _keep_latest(current_val, new_val):
      return new_val if new_val is not None else current_val

  class AgentState(TypedDict):
      market_data: Annotated[Optional[Dict[str, Any]], _keep_latest]
      sentiment_data: Annotated[Optional[Dict[str, Any]], _keep_latest]
  ```
* **Thread-Safe Checkpointing (`MemorySaver`):** Every analysis session is assigned a unique `thread_id` (e.g., `research_AAPL_20261008`), enabling independent concurrent sessions without cross-talk.
* **Streamlit Session State (`st.session_state`):** Engineered by **Sagar Trimukhe**, caches graph execution generators, intermediate streaming outputs, and resume flags across browser reruns.

---

# 11. Error Handling and Retry Mechanism

Engineered by **Nikhil Gaikwad**, **Shradha Gaikwad**, and **Ganesh Swami**, the codebase implements defensive engineering patterns:

1. **Gemini API Rate-Limit Resilience (100 RPM Regex Backoff):**
   * Google Gemini Free Tier limits requests to 100 per minute.
   * When embedding large 10-K filings (200+ chunks), the system catches HTTP 429 quota exceptions, parses Google's exact retry delay using regex (`seconds:\s*([0-9]+)`), pauses execution, and automatically retries without crashing.
2. **Dual-Strategy Comparative Valuation:**
   * If the LLM's function-calling tool invocation for `yfinance` encounters timeouts or formatting issues, `app/agents/comparative_analysis.py` catches the exception and immediately invokes a deterministic direct-API fallback.
3. **Target Price Float Sanitization:**
   * LLMs frequently return float strings with currency symbols or commas (e.g., `"$245.50"`). The Summary Agent passes all outputs through `_clean_target_price()` regex cleaners to guarantee valid numeric casting.
4. **Timezone Sanitization:**
   * Normalized all `yfinance` DatetimeIndex objects using `.tz_localize(None)` to prevent Streamlit visualization errors.
5. **Empty Vector Store Graceful Degradation:**
   * If an analyst queries a ticker whose documents have not yet been indexed in ChromaDB, the system warns the user cleanly rather than raising an unhandled retrieval exception.

---

# 12. AWS Deployment

The system is deployed on **Amazon Web Services (AWS)**, architected by **Ganesh Swami** with testing support from **Nikhil Gaikwad**:

### 12.1 AWS EC2 (Application Hosting)
* **Instance Type:** `t3.medium` (2 vCPUs, 4 GiB RAM, 20 GB gp3 SSD storage).
* **Operating System:** Ubuntu 22.04 LTS.
* **Automated Provisioning:** Created [`scripts/setup_ec2.sh`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/scripts/setup_ec2.sh) which automates Docker installation, swap space creation (2 GB), repository cloning, environment configuration, and `systemd` service setup.
* **Security Group Configuration:** Port `22` (SSH management) and Port `8501` (Streamlit web application).

### 12.2 AWS S3 (Scalable Document & Report Archiving)
* **S3 Bucket:** `ai-investment-research-repo`
* **Hierarchy:**
  * `s3://ai-investment-research-repo/filings/<TICKER>/` — archival storage for raw 10-K reports.
  * `s3://ai-investment-research-repo/reports/<TICKER>/` — signed investment memorandums.
* **Client Implementation:** [`app/integrations/s3_client.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/integrations/s3_client.py) wraps `boto3` with automatic offline fallbacks if AWS credentials are not configured.

### 12.3 Docker Containerization
* **Dockerfile:** Python 3.11-slim container with multi-stage dependency installation and non-root execution.
* **Docker Compose:** Configured `docker-compose.yml` mapping host port `8501:8501` and mounting volume `./data:/app/data` to ensure persistent ChromaDB state across container restarts.

---

