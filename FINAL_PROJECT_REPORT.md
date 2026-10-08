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

# 13. Sprint-Wise Progress

### Week 1 Progress (08 September – 15 September 2026)
* **Focus:** Project inception, problem scoping, system architecture, core configuration, Docker setup, baseline document ingestion, and initial agent nodes.
* **Key Achievements:** Selected Theme 15 (AI Investment Research Assistant under Finance Domain). Initialized project repository, Docker container setup, and configuration system (`app/core/config.py`, `app/core/state.py`). Connected Gemini LLM and persistent ChromaDB. Built initial document ingestion and agent nodes (`market_research`, `trend_analysis`).
* **Lead Contributors:** Ganesh Swami, Shradha Gaikwad, Nilanjan Das.

### Week 2 Progress (16 September – 23 September 2026)
* **Focus:** LangGraph workflow compilation, parallel fan-out/fan-in reducers, S3 client integration, and Streamlit dashboard prototype.
* **Key Achievements:** Assembled the compiled LangGraph workflow (`app/services/workflow_service.py`). Solved parallel state collisions using `_keep_latest` reducers. Integrated AWS S3 client and Markdown export service. Developed the interactive 3-tab Streamlit dashboard (`app/main.py`).
* **Lead Contributors:** Ganesh Swami, Sagar Trimukhe, Nikhil Gaikwad.

### Week 3 Progress (24 September – 01 October 2026)
* **Focus:** Mathematical volatility modeling, RAG metadata isolation, prompt engineering, and mid-capstone review.
* **Key Achievements:** Implemented 1-year stock price volatility (based on 252 trading days) and historical maximum price drop (drawdown). Validated strict metadata filtering in ChromaDB to prevent cross-ticker data contamination. Conducted mid-cohort review demonstration.
* **Lead Contributors:** Shradha Gaikwad, Nilanjan Das, Sagar Trimukhe.

### Week 4 Progress (02 October – 09 October 2026)
* **Focus:** AWS cloud deployment, expanded stock universe, official SEC EDGAR 10-K filings, testing, and final documentation.
* **Key Achievements:** Configured AWS EC2 automated provisioning script (`scripts/setup_ec2.sh`) and AWS S3 report archiving. Containerized with Docker. Expanded NASDAQ universe catalog to 270 stocks. Built official SEC EDGAR 10-K downloader and downloaded 20 genuine filings. Successfully verified Apple 10-K RAG retrieval. Compiled 72-slide presentation (`presentation.html`) and final capstone report.
* **Lead Contributors:** Ganesh Swami, Nikhil Gaikwad, Nilanjan Das, Sagar Trimukhe.

---

# 14. Screenshots and Demo Evidence

*(Embed the 4 mandatory screenshots captured from your live AWS deployment as outlined in Section 6 of `AWS_DEPLOYMENT_GUIDE.md`)*

1. **AWS EC2 Management Console Screenshot:** Demonstrating active `t3.medium` EC2 instance, public IPv4 address, and `2/2 checks passed` health status.
2. **AWS S3 Management Console Screenshot:** Demonstrating the `ai-investment-research-repo` bucket with `/filings/` and `/reports/` directories containing uploaded assets.
3. **AWS Security Group Configuration Screenshot:** Demonstrating inbound rule authorization for Port `8501` (Streamlit) and Port `22` (SSH).
4. **Live Streamlit Web Application Screenshot:** Demonstrating the active browser address bar at `http://<EC2_PUBLIC_IP>:8501` showing the research analysis results and HITL certification form.

# 15. Challenges Faced and Engineering Resolutions

During the design, implementation, and cloud deployment of the AI Investment Research Assistant, the team resolved 12 major engineering challenges:

| # | Challenge Category | Real-World Technical Problem Encountered | Concrete Engineering Resolution Implemented | Primary Lead |
|:---:|:---|:---|:---|:---|
| **1** | **LangGraph Concurrency** | **Parallel Fan-Out State Collisions:** When the Router node dispatched `market_research` and `trend_analysis` concurrently, both nodes completed asynchronously and attempted to update overlapping dictionary keys in `AgentState`. Standard LangGraph state merging failed with `InvalidUpdateError` due to undefined conflict resolution. | Implemented custom `_keep_latest(current_val, new_val)` reducers wrapped in `Annotated[Optional[Dict], _keep_latest]` in `app/core/state.py`. This explicitly instructs LangGraph how to merge concurrent parallel node outputs without race conditions. | Ganesh Swami |
| **2** | **API Quota Management** | **Gemini 100 RPM Free-Tier Quota Exhaustion:** A complete Form 10-K report exceeds 200,000 characters (~209 chunks). Ingesting these chunks generated rapid embedding requests that triggered Google GenAI HTTP 429 `RESOURCE_EXHAUSTED` errors, crashing document ingestion midway. | Built an adaptive batching engine in `app/services/document_ingestion.py`. Processed chunks in micro-batches of 20 with 1.0s pacing, and implemented regex-driven exponential backoff parsing Google's exact retry window (`seconds:\s*([0-9]+)`), automatically pausing and resuming without data loss. | Nikhil Gaikwad |
| **3** | **RAG Tabular Integrity** | **Financial Context Fragmentation in Document Chunking:** Naive text chunking (300–500 chars) split multi-column balance sheets and operating statements across arbitrary boundaries. Retrieved chunks contained floating financial figures without column headers, leading to extraction hallucinations. | Conducted empirical chunking evaluations across 500, 1000, 1500, and 2000 character windows. Standardized on **1,500 characters with 150-character (10%) overlap** using `RecursiveCharacterTextSplitter`, configuring double newlines (`\n\n`) as high-priority separators to preserve complete accounting tables. | Nilanjan Das |
| **4** | **Vector Store Isolation** | **Cross-Ticker Semantic Contamination in Multi-Company Index:** In a shared ChromaDB database containing multiple corporate filings (e.g., Apple, Meta, NVIDIA), semantic queries for "operating margin expansion" retrieved chunks from competing companies, causing hybrid hallucinated analyses. | Implemented mandatory metadata tagging during ingestion (`{"ticker": clean_ticker, "source": filename, "chunk_id": i}`). In `app/services/retrieval_service.py`, enforced strict ChromaDB metadata filters (`filter={"ticker": target_ticker}`), guaranteeing 100% data isolation per company. | Nilanjan Das |
| **5** | **Output Schema Sanitization** | **LLM String Output Breaking Mathematical Float Casting:** The Summary Agent's 12-month target price prompt frequently generated string-formatted outputs like `"$245.50"`, `"245.50 USD"`, or ranges (`"$240 - $260"`), causing Python `float()` casting to fail with `ValueError` in downstream volatility engines. | Engineered a defensive regex sanitizer (`_clean_target_price`) in `app/agents/summary_agent.py` that strips currency symbols, commas, and trailing text, computes the midpoint for range strings, and validates numeric bounds before invoking mathematical risk engines. | Shradha Gaikwad |
| **6** | **Telemetry Data Integrity** | **Timezone-Aware DatetimeIndex Crashing Streamlit Charts:** `yfinance` historical price data returns a Pandas DataFrame with timezone offsets (`America/New_York`). Passing this to Streamlit's `st.line_chart()` caused PyArrow serialization to throw `TypeError: Cannot serialize timezone-aware datetime index`. | Added automatic timestamp normalization in `app/integrations/market_data.py`, stripping timezone offsets using `.tz_localize(None)` while maintaining exact market date alignment, ensuring stable visual rendering across all browser sessions. | Nikhil Gaikwad |
| **7** | **SEC EDGAR Compliance** | **Automated Scraping Blocks (HTTP 403) & Gzip Stream Failures:** SEC EDGAR servers strictly block generic Python `urllib` User-Agents under its Fair Access Policy. Furthermore, valid responses returned compressed Gzip streams, resulting in binary decode exceptions in UTF-8 text decoders. | Formatted request headers declaring an institutional User-Agent (`AcademicResearchInvestmentAssistant/1.0`), throttled requests to <5 req/sec, and implemented transparent Gzip decompression detection checking magic bytes (`\x1f\x8b`) in `scripts/fetch_real_10k_filings.py`. | Nilanjan Das |
| **8** | **Tool Calling Resilience** | **Tool-Calling Timeouts & Hallucinated Argument Signatures:** When evaluating peer valuation multiples, relying solely on LLM function calling occasionally failed due to model parameter hallucination or API latency when fetching metrics for two equities simultaneously. | Engineered a **dual-strategy execution pattern** in `app/agents/comparative_analysis.py`. The agent attempts structured tool calling first; upon any timeout or parameter exception, it immediately triggers a deterministic direct-API fallback using pre-fetched `yfinance` metrics. | Nikhil Gaikwad |
| **9** | **Session State Persistence** | **Streamlit Browser Reruns Wiping HITL Interruption State:** Streamlit re-executes scripts top-to-bottom on every user click. When `langgraph.types.interrupt()` paused the workflow for human review, subsequent browser reruns created fresh thread instances, wiping the in-memory graph state. | Bound LangGraph's `MemorySaver` checkpointer to a persistent session thread identifier stored in `st.session_state`. When the analyst submits review decisions, the UI accesses the exact frozen thread ID and unfreezes the execution via `Command(resume=review_payload)`. | Sagar Trimukhe |
| **10** | **Cloud Degradation** | **Missing AWS Credentials Crashing Local Environments:** In local student development or offline demo environments without configured AWS IAM credentials, `boto3` threw unhandled `NoCredentialsError` during document ingestion and memorandum export. | Built a defensive wrapper in `app/integrations/s3_client.py` with `is_available()` health checks. When AWS credentials are absent, the system gracefully logs a non-blocking notice, maintains 100% local functionality, and disables the S3 export button with an informative tooltip. | Ganesh Swami |
| **11** | **Quantitative Modeling** | **Financial Volatility Calculation Skew from Non-Trading Days:** Calculating simple standard deviations of price changes over calendar date ranges skewed volatility metrics when weekends and market holidays created non-uniform time steps. | Calculated daily price changes over actual open market days and scaled them to a standard 252-day trading year to compute an accurate annual price risk score, alongside maximum historical price drop. | Shradha Gaikwad |
| **12** | **Global Equity Filings** | **Foreign Private Issuer SEC Form Discrepancies (10-K vs. 20-F):** Global market leaders listed on NASDAQ (such as ASML or Arm Holdings) file Form 20-F rather than domestic Form 10-K, causing standard 10-K search queries to return empty records. | Built an intelligent discovery hierarchy in `fetch_real_10k_filings.py` and `nasdaq_universe.py` that queries Form 10-K, falls back to amended 10-K/A, and automatically handles Form 20-F annual disclosures for foreign private issuers. | Nilanjan Das |

---

# 16. Key Learnings

1. **Stateful Graphs vs. Conversational Loops:** Stateful graphs like LangGraph provide superior determinism, auditability, and safety compared to open-ended conversational agent loops for financial applications.
2. **Chunking Trade-offs in Financial RAG:** Small chunk sizes (300–500 chars) fragment financial balance sheets and disclosure notes. A 1,500-character chunk with 10% overlap is the mathematical sweet spot for preserving tabular context in SEC 10-K filings.
3. **Importance of Human-in-the-Loop Governance:** Autonomous AI must be bound by human review gates in high-stakes domains like finance to ensure accountability, regulatory compliance, and analyst confidence.
4. **Cloud Production Hardening:** Building resilient enterprise AI requires graceful degradation patterns — such as deterministic tool fallbacks, rate-limit backoff engines, and offline-capable cloud storage clients.

---

# 17. Future Scope

1. **Multimodal SEC Table Extraction:** Integrate vision-language models (e.g., Gemini Flash Vision) to directly parse complex rasterized financial tables, charts, and balance sheet exhibits in PDF filings.
2. **Automated SEC EDGAR Webhooks:** Connect SEC RSS feeds to automatically trigger the ingestion and research pipeline the instant an enterprise files a new 10-K or 8-K report.
3. **Advanced Portfolio Risk Optimization:** Expand beyond single-stock valuation to multi-stock portfolio optimization, calculating covariance matrices and Value-at-Risk (VaR) across an entire portfolio.
4. **Automated CI/CD Deployment:** Implement GitHub Actions pipelines to automatically test, build, and deploy new Docker containers to AWS EC2 upon git push.

---

# 18. Individual Contributions

Each team member contributed across their primary specialization and collaborated on cross-functional integration needs:

| Team Member | Primary Domain | Core Technical & Cross-Functional Contributions | Key Code Modules |
|:---|:---|:---|:---|
| **Ganesh Swami** | **Backend Architecture & DevOps Lead** | • Designed LangGraph Directed Acyclic Graph (DAG) state topology.<br>• Implemented parallel fan-out and fan-in synchronization with custom `_keep_latest` state reducers.<br>• Built Human-in-the-Loop (HITL) interrupt protocol (`langgraph.types.interrupt`) and resumption handling.<br>• Authored automated AWS EC2 provisioning script (`setup_ec2.sh`) and AWS S3 integration client.<br>• Cross-support: Collaborated with Sagar on Streamlit execution streaming and thread checkpointing. | `app/services/workflow_service.py`<br>`app/core/state.py`<br>`app/agents/hitl_review.py`<br>`scripts/setup_ec2.sh`<br>`app/integrations/s3_client.py` |
| **Shradha Gaikwad** | **Agent Intelligence & Financial Modeling Lead** | • Developed Market Research Agent for fundamental accounting and 10-K balance sheet extraction.<br>• Built Trend & Sentiment Analysis Agent with macroeconomic catalyst scoring (-1.0 to +1.0).<br>• Implemented Summary Agent investment thesis synthesis (BUY/HOLD/SELL rating & 12-month target price).<br>• Engineered stock risk calculations: 1-year annualized price volatility (based on 252 trading days) and historical maximum price drop (drawdown).<br>• Designed strongly typed Pydantic output validation contracts and defensive regex float sanitizers. | `app/agents/market_research.py`<br>`app/agents/trend_analysis.py`<br>`app/agents/summary_agent.py`<br>`app/schemas/financial.py`<br>`app/schemas/report.py` |
| **Sagar Trimukhe** | **Frontend UI & Chatbot/HITL Integration Lead** | • Built comprehensive 3-Tab Streamlit dashboard interface (`app/main.py`).<br>• Developed Document Ingestion UI with drag-and-drop file upload and ChromaDB status metrics.<br>• Engineered real-time agent execution visualizer and live node progress streaming.<br>• Built Human-in-the-Loop Analyst Review workspace with thesis editor and certification form.<br>• Integrated one-click Markdown memorandum export and AWS S3 cloud archiving buttons.<br>• Cross-support: Integrated Nilanjan's 270-stock catalog into the frontend quick-ingestion selector. | `app/main.py`<br>`app/services/export_service.py`<br>`presentation.html` |
| **Nilanjan Das** | **Data Engineering & Filing Ingestion Lead** | • Curated and implemented the 270-stock NASDAQ universe catalog across 6 major industries.<br>• Developed automated SEC EDGAR 10-K downloader with accession number tracking and HTML-to-text cleaning.<br>• Downloaded, verified, and cataloged 20 genuine official SEC Form 10-K filings.<br>• Engineered recursive text splitting (1,500 chars / 150 overlap) optimized for financial tables.<br>• Implemented persistent ChromaDB storage with ticker metadata isolation to eliminate cross-stock contamination. | `app/services/nasdaq_universe.py`<br>`scripts/fetch_real_10k_filings.py`<br>`app/services/document_ingestion.py`<br>`app/integrations/vector_store.py` |
| **Nikhil Gaikwad** | **Full-Stack Integration, Telemetry & QA Engineer** | • Integrated `yfinance` live market telemetry tools for real-time stock profiles, trailing/forward P/E, and EV/EBITDA.<br>• Implemented Comparative Valuation Agent with dual-strategy tool calling and deterministic direct-API fallback.<br>• Built Gemini Free-Tier rate-limit resilience engine with regex-driven exponential backoff (100 RPM recovery).<br>• Resolved Streamlit DatetimeIndex timezone rendering bugs via `.tz_localize(None)`.<br>• Developed RAG evaluation benchmark test scripts and led end-to-end integration testing. | `app/agents/comparative_analysis.py`<br>`app/integrations/market_data.py`<br>`app/tools/financial_tools.py`<br>`app/evaluation/rag_eval.py`<br>`scripts/test_aws_s3.py` |
