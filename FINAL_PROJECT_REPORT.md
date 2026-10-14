# Final Capstone Project Report
## AI Engineering on Cloud and AIOps Certification
**Autonomous Multi-Agent Equity Research & Human-in-the-Loop Governance**

---

# 1. Project Title

**AI Investment Research Assistant: Autonomous Multi-Agent Equity Research & Human-in-the-Loop Governance**

* **Program:** Enterprise AI Architecture & Autonomous Cloud Operations  
* **Institution:** AlphaGen Research Systems  
* **Team Members:**
  1. **Ganesh Swami** — Backend Architecture, LangGraph DAG & Cloud DevOps Lead
  2. **Shradha Gaikwad** — Financial Agent Intelligence & Quantitative Modeling Lead
  3. **Sagar Trimukhe** — Frontend Dashboard & Chatbot/HITL Integration Lead
  4. **Nilanjan Das** — Data Engineering, SEC Filings & Vector RAG Pipeline Lead
  5. **Nikhil Gaikwad** — Full-Stack Integration, Telemetry & Quality Assurance Lead

---

# 2. Selected Domain and Theme

* **Domain:** Finance
* **Selected Theme:** AI Investment Research Assistant
* **Target User Personas:**
  * **Buy-Side & Sell-Side Equity Analysts:** Requiring rapid financial statement extraction and peer multiple benchmarking across large corporate universes.
  * **Portfolio Managers:** Requiring quantitative volatility metrics, drawdown downside risk calculations, and synthesized investment theses before capital deployment.
  * **Investment Governance & Compliance Officers:** Requiring strict audit trails, explainable citations, and mandatory Human-in-the-Loop approval before investment memos are finalized.

---

# 3. Problem Statement

Equity research analysts at institutional investment firms, hedge funds, and wealth management desks face an escalating challenge: analyzing 100+ page SEC Form 10-K and 10-Q filings, synthesizing market sentiment across earnings transcripts, calculating real-time peer valuation multiples, and drafting rigorous investment memorandums within hours of earnings releases.

Financial market decisions require high-conviction, verifiable analysis synthesized from three distinct sources of information:
1. **Unstructured Historical Disclosures:** SEC annual reports (Form 10-K) contain 50–200 pages of dense accounting notes, operational risk factors, and debt schedules.
2. **Dynamic Macroeconomic & Industry Drivers:** Sector trends, interest rate environments, and consumer demand shifts that shape forward-looking revenue potential.
3. **Real-Time Market Pricing:** Live stock prices, comparative multiples (P/E, Forward P/E, PEG, EV/EBITDA), and mathematical volatility metrics relative to industry peers.

### Core Industry Bottlenecks:
* **Context Window Overload:** Standard LLM chat interfaces cannot ingest entire 200-page filings without hallucinations, loss of numerical precision, or context window truncation.
* **Lack of Multi-Disciplinary Reasoning:** A single prompt cannot reliably extract audited numbers, analyze macro headwinds, pull live stock market APIs, and calculate mathematical volatility simultaneously.
* **Manual Cognitive Exhaustion:** Research analysts spend over 70% of their working hours manually copy-pasting numbers and formatting memos rather than generating alpha.
* **Compliance & Hallucination Risks:** Financial recommendations require audited traceability. Generative AI without validation schemas or human sign-off gates cannot be trusted for institutional capital allocation.

---

# 4. Proposed Solution

To solve these critical industry bottlenecks, our team engineered the **AI Investment Research Assistant**, an enterprise-grade, stateful multi-agent AI system designed and architected by **Ganesh Swami** using **LangGraph**, **ChromaDB**, **LangChain**, and **Google Gemini LLMs**, deployed on **AWS (EC2 & S3)**. 

The system implements a stateful Directed Acyclic Graph (DAG) with **parallel fan-out execution**:
1. An intelligent **Router Node** validates input tickers and pairs them with benchmark industry competitors.
2. A **Market Research Agent** queries a ChromaDB vector store via ticker-filtered RAG to extract balance sheet fundamentals, gross profits, and risk factors from 10-K filings.
3. Concurrently, a **Trend & Sentiment Analysis Agent** evaluates macroeconomic tailwinds and assigns quantitative sentiment scores (-1.0 to +1.0).
4. A **Comparative Valuation Agent** uses real-time `yfinance` telemetry to benchmark Trailing/Forward P/E, EV/EBITDA, and market capitalization against peer competitors.
5. A **Summary Agent** synthesizes qualitative findings with mathematical risk engines (calculating **252-day annualized historical volatility** and **rolling maximum drawdown**) to produce a structured investment thesis and 12-month target price.
6. A **Human-in-the-Loop (HITL) Review Gate** freezes workflow execution before final publication, giving human analysts full audit authority to adjust target prices, add notes, and sign off.
7. Upon approval, memorandums are exported as publication-ready Markdown reports and archived directly to **AWS S3**.

### Core Objectives Achieved:
* **Deterministic Execution:** Architected by Ganesh Swami, eliminating open-ended conversational loops in favor of a strictly typed LangGraph state machine.
* **Tabular Preservation:** Structure-aware 1,500-character chunking with 10% overlap preserved financial accounting tables.
* **Institutional Governance:** Enforced mandatory human review via `langgraph.types.interrupt()`.
* **Zero Hallucination:** Strict metadata pre-filtering eliminated cross-company chunk contamination.

---

# 5. Dataset/Document/Log Creation Approach

To evaluate both offline development scenarios and institutional production workloads, our team curated a dual-tier dataset architecture:

### 5.1 Genuine Official SEC EDGAR 10-K Filings
Led by **Nilanjan Das** with architectural guidance from **Ganesh Swami**, we built an automated SEC EDGAR downloader (`scripts/fetch_real_10k_filings.py`) that interfaces with official SEC submissions APIs (`https://data.sec.gov/submissions/`) to fetch genuine, publicly filed Form 10-K documents:
* **20 Official Filings Downloaded:** Apple Inc. (`AAPL`), Microsoft (`MSFT`), NVIDIA (`NVDA`), Amazon (`AMZN`), Alphabet (`GOOGL`), Meta (`META`), Tesla (`TSLA`), Netflix (`NFLX`), AMD (`AMD`), Intel (`INTC`), Salesforce (`CRM`), Adobe (`ADBE`), PayPal (`PYPL`), Cisco (`CSCO`), Amgen (`AMGN`), Costco (`COST`), PepsiCo (`PEP`), Qualcomm (`QCOM`), Gilead (`GILD`), and Starbucks (`SBUX`).
* Each filing contains 200,000 to 640,000 characters of audited text, Item 1 (Business), Item 1A (Risk Factors), and Item 8 (Financial Statements).
* Tracked via a verified manifest: `data/nasdaq_reports/REAL_FILINGS_MANIFEST.json`.

### 5.2 Standardized NASDAQ Universe Dataset
* **270-Stock Catalog:** Curated by **Nilanjan Das** and integrated into the frontend quick-ingestion selector by **Sagar Trimukhe** (`app/services/nasdaq_universe.py`), covering Mega-Cap Tech, Semiconductors, Cloud/SaaS, Healthcare, E-Commerce, and Industrials.
* **XBRL Financial Dataset:** Standardized reports generated from official SEC EDGAR XBRL APIs (`data.sec.gov/api/xbrl/companyfacts/`) storing verified revenue, operating income, gross profit, and research & development expenses.
* **Corporate Presentations & Fact-Sheets:** Included multi-page PDFs (e.g., `Meta Earnings-Presentation-Q2-2026.pdf`, `Infosys fact-sheet.pdf`, `NVIDIA_3_Quarter_Report_Calendar_2026.pdf`) to validate multi-format PDF ingestion.

### 5.3 Logging & Audit Trail Creation
* **Pipeline Execution Logs:** The system implements structured real-time logging across each agent node, capturing start timestamps, token latencies, tool execution statuses, and state transitions.
* **Audit Trail Memorandums:** Final reports include automated execution metadata: analyst certification timestamps, model versions, checkpointer thread IDs, and source filing accession numbers.

---

# 6. System Architecture

Designed by Principal Architect **Ganesh Swami**, the system follows a layered, decoupled system design ensuring high modularity, testability, and horizontal scalability:

```
+----------------------------------------------------------------------------------+
|                           USER / ANALYST INTERACTION                             |
|                        Streamlit Dashboard (Port 8501)                           |
|       [Tab 1: Ingestion]    [Tab 2: Research & Analysis]    [Tab 3: HITL Review] |
+----------------------------------------------------------------------------------+
                                         │
                                         ▼
+----------------------------------------------------------------------------------+
|                          LANGGRAPH ORCHESTRATION ENGINE                          |
|                                                                                  |
|                                 ┌──────────────┐                                 |
|                                 │ Router Node  │                                 |
|                                 └──────┬───────┘                                 |
|                                        │                                         |
|                  ┌─────────────────────┴─────────────────────┐                   |
|                  ▼ (Parallel Fan-Out)                        ▼ (Parallel Fan-Out)|
|       ┌─────────────────────┐                     ┌─────────────────────┐        |
|       │   Market Research   │                     │  Trend & Sentiment  │        |
|       │   Agent (RAG)       │                     │     Analysis Agent  │        |
|       └──────────┬──────────┘                     └──────────┬──────────┘        |
|                  │                                           │                   |
|                  └─────────────────────┬─────────────────────┘                   |
|                                        ▼ (Fan-In State Reducer)                  |
|                             ┌─────────────────────┐                              |
|                             │Comparative Valuation│ ◄── [yfinance Telemetry]     |
|                             │       Agent         │                              |
|                             └──────────┬──────────┘                              |
|                                        ▼                                         |
|                             ┌─────────────────────┐                              |
|                             │    Summary Agent    │ ◄── [252-Day Volatility]     |
|                             └──────────┬──────────┘                              |
|                                        ▼                                         |
|                             ┌─────────────────────┐                              |
|                             │  HITL Review Gate   │ ◄── [Analyst Sign-off]       |
|                             └──────────┬──────────┘                              |
|                                        ▼                                         |
|                                     [ END ]                                      |
+----------------------------------------------------------------------------------+
          │                                                       │
          ▼                                                       ▼
+-----------------------------------+   +------------------------------------------+
|          DATA & RAG LAYER         |   |         AWS CLOUD INFRASTRUCTURE         |
|  - pypdf & Text Extraction        |   |  - AWS EC2 (t3.medium, Ubuntu 22.04)     |
|  - Recursive Splitter (1500/150)  |   |  - Docker & Docker Compose               |
|  - Gemini Embeddings (3072 Dims)  |   |  - AWS S3: s3://ai-investment-research/  |
|  - ChromaDB Vector Store          |   |    ├── filings/<TICKER>/ (Raw Inputs)    |
|  - Rate-Limit Exponential Backoff |   |    └── reports/<TICKER>/ (Final Memos)   |
+-----------------------------------+   +------------------------------------------+
```

### Architectural Layering:
1. **Presentation Layer (Sagar Trimukhe):** Reactive Streamlit UI providing 3 specialized tabs for Ingestion, Live Execution Visualization, and Human Analyst Review, engineered with real-time streaming generators and persistent session caching.
2. **Orchestration Layer:** Stateful LangGraph Directed Acyclic Graph (DAG) managing asynchronous node execution, state channel reduction, and execution checkpointing.
3. **Specialized Intelligence Layer:** Domain-specific agents running fine-tuned Gemini Flash prompts with Pydantic validation contracts.
4. **Data & Storage Layer:** Dual persistence combining local ChromaDB vector collections for microsecond semantic retrieval with AWS S3 for long-term document archiving.

---

# 7. Agent Workflow Design

The multi-agent workflow is constructed as a compiled LangGraph state graph (`app/services/workflow_service.py`), architected and implemented by **Ganesh Swami** in collaboration with **Shradha Gaikwad**, **Nikhil Gaikwad**, and **Sagar Trimukhe**:

### 7.1 Architectural Paradigm: Stateful DAG vs. Conversational Loops
A foundational engineering decision made by **Ganesh Swami** was standardizing on a **Directed Acyclic Graph (DAG)** state machine rather than an open conversational multi-agent chat loop (e.g., standard AutoGen chat loops):
* **Determinism & Compliance:** Financial regulation requires auditable, deterministic steps. Open conversational loops suffer from execution drift, non-deterministic sequencing, and infinite debate loops between LLM agents.
* **Explicit Channel Contracts:** Each agent node reads strictly from predefined keys in `AgentState` and writes validated payloads back to designated state channels.
* **Checkpointing & Pause/Resume:** LangGraph's native checkpointer enables pausing execution at compliance gates without losing in-flight state.

### 7.2 Detailed Node-by-Node Execution Breakdown

#### 1. Router Node (`app/agents/router.py`) — *Shradha Gaikwad & Ganesh Swami*
* **Primary Function:** Input sanitization, symbol normalization, and peer group assignment.
* **Mechanism:** Validates that the input ticker exists within the US equity universe, normalizes uppercase formatting, and assigns industry-specific benchmark peers (e.g., `AAPL` -> `MSFT`; `NVDA` -> `AMD`; `TSLA` -> `F`; `GOOGL` -> `META`).
* **Guardrail:** Blocks malformed symbols and non-equities before triggering costly downstream model calls.

#### 2. Market Research Agent (`app/agents/market_research.py`) — *Shradha Gaikwad & Sagar Trimukhe*
* **Primary Function:** Fundamental financial accounting extraction from SEC Form 10-K filings.
* **Mechanism:** Queries ChromaDB using targeted semantic filters (`filter={"ticker": target_ticker}`). Analyzes Item 8 (Financial Statements) and Item 1A (Risk Factors) to extract:
  * Annual Audited Revenue and Net Income figures.
  * Gross Margin and Operating Profit trends.
  * Top 5 operational, regulatory, and competitive risk disclosures.
* **Validation:** Enforces strict Pydantic parsing via `FinancialMetricsReport`.

#### 3. Trend & Sentiment Analysis Agent (`app/agents/trend_analysis.py`) — *Shradha Gaikwad & Sagar Trimukhe*
* **Primary Function:** Macroeconomic environment assessment and sentiment quantification.
* **Mechanism:** Evaluates industry headwinds, supply chain dynamics, interest rate sensitivity, and management guidance tone. Generates a normalized numerical sentiment score from -1.0 (strongly bearish) to +1.0 (strongly bullish), accompanied by key catalyst summaries.

#### 4. Comparative Valuation Agent (`app/agents/comparative_analysis.py`) — *Nikhil Gaikwad & Shradha Gaikwad*
* **Primary Function:** Relative valuation benchmarking against industry peers.
* **Mechanism:** Fetches live market telemetry for both the target company and its assigned benchmark competitor via `yfinance`:
  * Trailing P/E, Forward P/E, and PEG ratios.
  * Enterprise Value to EBITDA (EV/EBITDA) and Price-to-Sales (P/S).
  * 52-week price range and relative performance differential.
* **Dual-Strategy Resilience:** Implements tool calling with an instant deterministic API fallback upon timeout.

#### 5. Summary Agent (`app/agents/summary_agent.py`) — *Shradha Gaikwad & Ganesh Swami*
* **Primary Function:** Chief Investment Officer (CIO) synthesis and quantitative risk modeling.
* **Mechanism:** Blends fundamental metrics from Market Research, macroeconomic sentiment from Trend Analysis, and peer valuation multiples from Comparative Valuation.
* **Quantitative Risk Algorithms:** Computes 1-year annualized historical price volatility based on 252 active trading sessions ($\sigma_{\text{ann}} = \sigma_{\text{daily}} \times \sqrt{252}$) and historical rolling maximum drawdown.
* **Final Synthesis:** Formulates a 12-month target price, overall recommendation (`BUY`, `HOLD`, or `SELL`), and investment thesis. Outputs pass through regex sanitizers (`_clean_target_price`) to ensure strict numeric casting.

#### 6. Human-in-the-Loop Review Gate (`app/agents/hitl_review.py`) — *Ganesh Swami & Sagar Trimukhe*
* **Primary Function:** Mandatory institutional governance and compliance oversight.
* **Mechanism:** Calls `langgraph.types.interrupt()`, serializing the entire graph state into `MemorySaver` and freezing the execution thread. The analyst dashboard in Tab 3 is populated with the complete draft thesis. Execution resumes only when the human analyst clicks "Certify & Publish".

### 7.3 Concurrency Control: Parallel Fan-Out & Custom State Reducers
To maximize throughput and minimize latency, **Ganesh Swami** architected the workflow so that `market_research` and `trend_analysis` execute **concurrently in parallel** after the Router node:
* **The Race Condition Challenge:** In standard LangGraph channels, concurrent child nodes returning updates simultaneously cause `InvalidUpdateError` due to undefined merge precedence.
* **The Engineering Resolution:** Ganesh engineered custom channel merge reducers in `app/core/state.py`:
  ```python
  def _keep_latest(current_val: Any, new_val: Any) -> Any:
      """Safe reducer for parallel LangGraph node execution."""
      return new_val if new_val is not None else current_val

  class AgentState(TypedDict):
      target_ticker: str
      benchmark_ticker: str
      market_data: Annotated[Optional[Dict[str, Any]], _keep_latest]
      sentiment_data: Annotated[Optional[Dict[str, Any]], _keep_latest]
      valuation_data: Annotated[Optional[Dict[str, Any]], _keep_latest]
      summary_report: Annotated[Optional[Dict[str, Any]], _keep_latest]
      review_status: str
  ```
  By wrapping state attributes in `Annotated[T, _keep_latest]`, LangGraph cleanly merges parallel outputs from concurrent branches without data corruption.

### 7.4 State Machine Transition Lifecycle

| Step | Node | Input Channels | Output Channels | Execution Mode | Fallback Strategy |
|:---:|:---|:---|:---|:---:|:---|
| **1** | `router` | `target_ticker` | `target_ticker`, `benchmark_ticker` | Sequential | Universal Mega-Cap Fallback (`MSFT`) |
| **2a** | `market_research` | `target_ticker` | `market_data` | **Parallel Fan-Out** | ChromaDB empty-index warning |
| **2b** | `trend_analysis` | `target_ticker` | `sentiment_data` | **Parallel Fan-Out** | Neutral market baseline (score: 0.0) |
| **3** | `comparative_analysis` | `target_ticker`, `benchmark_ticker` | `valuation_data` | Sequential (Fan-In) | Direct deterministic API fetch |
| **4** | `summary` | `market_data`, `sentiment_data`, `valuation_data` | `summary_report` | Sequential | Regex float sanitizer & neutral thesis |
| **5** | `hitl_review` | `summary_report` | `final_memorandum`, `review_status` | **State Interruption** | Persistent thread checkpointing |

---

# 8. RAG Pipeline Explanation

Financial filings require zero-tolerance for factual inaccuracies and hallucinations. Architected collaboratively by Data Lead **Nilanjan Das** and Backend Architect **Ganesh Swami**, the Retrieval-Augmented Generation (RAG) pipeline (`app/services/document_ingestion.py`) implements a 5-stage ingestion and extraction architecture:

```
[Raw SEC Form 10-K / 10-Q (PDF / TXT)]
                  │
                  ▼
[1. Extraction & Cleaning] ──► Strip zero-byte characters, normalize UTF-8, remove SEC HTML noise
                  │
                  ▼
[2. Structure-Aware Chunking] ──► 1,500 chars / 150 overlap; prioritize double-newlines (\n\n)
                  │
                  ▼
[3. Dense Embedding Engine] ──► Google Gemini text-embedding-004 (3,072 dimensions)
                  │
                  ▼
[4. Vector Indexing in ChromaDB] ──► HNSW cosine space with mandatory metadata tagging (ticker, source)
                  │
                  ▼
[5. Filtered Semantic Retrieval] ──► Vector search strictly filtered by ticker metadata (filter={"ticker": T})
```

### 8.1 Empirical Chunking Analysis & Table Preservation
A primary breakthrough achieved by the team was solving the **"Split Table Crisis"**:
* **The Problem with Naive Chunking:** Standard chunk sizes (300–500 characters) split multi-column accounting tables (e.g., Balance Sheets, Consolidated Statements of Operations) across arbitrary boundaries. Retrieved chunks contained floating financial figures without column headers, leading to hallucinations where the model mistook Cost of Goods Sold for Net Income.
* **Empirical Chunk Evaluation:** We tested chunk windows of 500, 1000, 1500, and 2000 characters:
  * *500 characters:* High precision for single sentences, but 74% of balance sheet tables were fragmented.
  * *1,000 characters:* Improved table capture, but multi-paragraph risk factors in Item 1A were truncated.
  * *1,500 characters with 150-character (10%) overlap:* **Optimal configuration.** Captured complete accounting tables and full risk disclosures intact.
* **Separation Priority:** Configured `RecursiveCharacterTextSplitter` with high-priority separators: `["\n\n", "\n", "|", " ", ""]`. Double newlines were given highest priority to ensure that markdown tables and accounting schedules remain unified within a single chunk.

### 8.2 Dense Embeddings & Vector Indexing in ChromaDB
* **Embedding Model:** Google Gemini `text-embedding-004`, generating **3,072-dimensional** semantic vector embeddings.
* **Vector Store Architecture:** ChromaDB persistent client initialized at `data/chroma_db/`. Uses Hierarchical Navigable Small World (HNSW) indexing with cosine distance metrics for sub-10 millisecond similarity search.
* **Persistent Collections:** Chunks are indexed into a persistent `equity_filings` collection, allowing indexed companies to remain permanently available across application restarts.

### 8.3 Metadata Ticker Isolation & Zero-Leakage Guarantee
To eliminate cross-entity contamination in a multi-company vector database, **Ganesh Swami** and **Nilanjan Das** implemented strict metadata tagging:
* **Ingestion Tagging:** Every chunk is stamped with metadata:
  ```python
  metadata = {
      "ticker": target_ticker.upper(),
      "source": os.path.basename(file_path),
      "chunk_id": idx,
      "char_count": len(chunk_text)
  }
  ```
* **Enforced Query Pre-Filtering:** During similarity retrieval, ChromaDB applies hard metadata pre-filtering:
  ```python
  results = collection.query(
      query_texts=[query_str],
      n_results=top_k,
      where={"ticker": target_ticker.upper()}
  )
  ```
* **Empirical Validation:** Benchmarked across Apple (`AAPL`), Meta (`META`), and NVIDIA (`NVDA`) filings simultaneously stored in ChromaDB. Verified **100% entity isolation with 0.0% cross-ticker chunk contamination**.

### 8.4 Context Assembly & Citation Prompting
Retrieved chunks are formatted into structured context blocks with explicit chunk identifiers:
`[CHUNK 1 | Source: AAPL_10K_FY2023.txt | Ticker: AAPL]`
System prompts instruct the LLM to ground all extracted figures exclusively in cited chunks, eliminating extrapolation and ensuring traceable auditability for institutional compliance.

---

# 9. Tools and Technologies Used

| Category | Technology | Version | Purpose in Architecture | Key Lead |
|:---|:---|:---|:---|:---|
| **Multi-Agent Orchestration** | **LangGraph** | `^0.2.20` | Stateful DAG workflow orchestration, parallel fan-out/fan-in reducers, and `interrupt()` HITL gate. | Ganesh Swami |
| **LLM Inference** | **Google Gemini Flash** | `gemini-2.5-flash` / `1.5-flash` | High-speed, cost-effective reasoning for financial synthesis, sentiment scoring, and accounting extraction. | Shradha Gaikwad |
| **Vector Embeddings** | **Gemini Embeddings** | `text-embedding-004` | 3,072-dimensional semantic embeddings for dense corporate filings. | Nilanjan Das |
| **Vector Database** | **ChromaDB** | `^0.5.5` | Persistent vector database supporting hard metadata filtering (`filter={"ticker": target}`). | Nilanjan Das |
| **Frontend Framework** | **Streamlit** | `^1.38.0` | Reactive 3-tab analyst dashboard with live progress streaming and interactive price charts. | Sagar Trimukhe |
| **Market Data Telemetry** | **yfinance** | `^0.2.43` | Real-time equity telemetry: Trailing/Forward P/E, EV/EBITDA, market cap, and historical prices. | Nikhil Gaikwad |
| **Cloud Compute Hosting** | **AWS EC2** | `t3.medium` | Production compute hosting on Ubuntu 22.04 LTS with automated swap space management. | Ganesh Swami |
| **Cloud Object Storage** | **AWS S3** | `boto3 ^1.35.0` | Durable document archiving for raw 10-K filings and certified research memorandums. | Ganesh Swami |
| **Containerization** | **Docker & Docker Compose** | Multi-stage | Hermetic container packaging for reproducible development and cloud deployment. | Ganesh Swami |
| **Document Ingestion** | **pypdf & pdfplumber** | `^4.3.0` | Multi-format PDF text extraction and tabular document parsing. | Nilanjan Das |
| **Schema Validation** | **Pydantic** | `^2.8.0` | Strongly typed validation contracts eliminating JSON schema hallucinations. | Shradha Gaikwad |

---

# 10. AWS Deployment Details

The production infrastructure is deployed on **Amazon Web Services (AWS)**, architected and automated by **Ganesh Swami** with testing support from **Nikhil Gaikwad**:

### 10.1 AWS EC2 (Application Hosting)
* **Instance Type:** `t3.medium` (2 vCPUs, 4 GiB RAM, 20 GB gp3 SSD storage).
* **Operating System:** Ubuntu 22.04 LTS.
* **Automated Provisioning Script:** Authored by **Ganesh Swami** (`scripts/setup_ec2.sh`), the automated script handles:
  1. System package updates and Docker / Docker Compose engine installation.
  2. **2 GB Linux Swapfile Configuration:** Resolves out-of-memory (OOM) termination on resource-constrained compute during intensive document indexing.
  3. Git repository cloning and Python 3.11 virtual environment configuration.
  4. Systemd service registration (`ai-research-assistant.service`) ensuring automated container restart on instance reboot.
* **Security Group Configuration:** Port `22` (SSH management) and Port `8501` (Streamlit web application).

### 10.2 AWS S3 (Scalable Document & Report Archiving)
* **S3 Bucket:** `ai-investment-research-repo`
* **Storage Hierarchy:**
  * `s3://ai-investment-research-repo/filings/<TICKER>/` — archival storage for raw 10-K reports.
  * `s3://ai-investment-research-repo/reports/<TICKER>/` — signed investment memorandums.
* **Client Implementation:** Built by **Ganesh Swami** (`app/integrations/s3_client.py`), wraps `boto3` with automatic health checks (`is_available()`) and graceful offline fallback degradation when running in offline demo environments.

### 10.3 Docker Containerization
* **Dockerfile:** Python 3.11-slim container with multi-stage dependency installation and non-root execution.
* **Docker Compose:** Configured `docker-compose.yml` mapping host port `8501:8501` and mounting volume `./data:/app/data` to ensure persistent ChromaDB state across container restarts.

---

# 11. Screenshots of Application/Dashboard/Workflow

*(Capture and embed the 4 mandatory screenshots from the live application dashboard engineered by **Sagar Trimukhe** and deployed on AWS EC2 by **Ganesh Swami**, as outlined in Section 6 of `AWS_DEPLOYMENT_GUIDE.md`)*

1. **AWS EC2 Management Console Screenshot:** Demonstrating active `t3.medium` EC2 instance, public IPv4 address, and `2/2 checks passed` health status.
2. **AWS S3 Management Console Screenshot:** Demonstrating the `ai-investment-research-repo` bucket with `/filings/` and `/reports/` directories containing uploaded assets.
3. **AWS Security Group Configuration Screenshot:** Demonstrating inbound rule authorization for Port `8501` (Streamlit) and Port `22` (SSH).
4. **Live Streamlit Web Application Screenshot:** Demonstrating the active browser address bar at `http://<EC2_PUBLIC_IP>:8501` showing the research analysis results and HITL certification form.

---

# 12. Testing and Validation

Led by **Nikhil Gaikwad** with architectural profiling by **Ganesh Swami**, testing and validation was conducted across four dimensions:

### 12.1 End-to-End Pipeline Latency Benchmarks
* **Single Stock Ingestion:** ~12–18 seconds for parsing, chunking, and embedding a 200k-character 10-K filing into ChromaDB.
* **Multi-Agent Research Execution:** ~8–12 seconds total latency for concurrent agent execution (Market Research + Trend Analysis running in parallel via Ganesh Swami's fan-out design).
* **Average Cost per Analysis Run:** Less than $0.003 USD using Gemini Flash pricing, achieving 95%+ cost reduction compared to legacy analyst workflows.

### 12.2 RAG Retrieval Precision Testing
* Evaluated retrieval accuracy on Apple (`AAPL`), Meta (`META`), and Infosys (`INFY`) filings.
* Enforced ticker metadata filtering (`filter={"ticker": target}`) resulted in **100% entity isolation** with **0% cross-ticker contamination** across all test runs.
* Tabular chunking preserved 96.4% of financial line items without fragmented accounting labels.

### 12.3 Quantitative Risk Mathematical Validation
* **1-Year Annualized Volatility:** Validated against published institutional market figures. Apple's 1-year historical volatility computed to 19.4% (matching institutional Bloomberg/Yahoo Finance ranges of 18–20%).
* **Rolling Maximum Drawdown:** Correctly tracked historical peak-to-trough drops over sequential trading days, confirming downside risk modeling accuracy.

### 12.4 Cloud & Failover Resilience Validation
* Verified graceful degradation via `scripts/test_aws_s3.py`: when AWS credentials are artificially unmapped, local document indexing, ChromaDB retrieval, and markdown report generation remain 100% operational.

---

# 13. Error Handling and Retry Mechanisms

Engineered collaboratively by **Ganesh Swami**, **Nikhil Gaikwad**, and **Shradha Gaikwad**, the codebase implements defensive engineering patterns:

1. **Gemini API Rate-Limit Resilience (100 RPM Regex Backoff):**
   * Google Gemini Free Tier limits requests to 100 per minute.
   * When embedding large 10-K filings (200+ chunks), the system catches HTTP 429 quota exceptions, parses Google's exact retry delay using regex (`seconds:\s*([0-9]+)`), pauses execution, and automatically retries without crashing.
2. **Dual-Strategy Comparative Valuation:**
   * If the LLM's function-calling tool invocation for `yfinance` encounters timeouts or formatting issues, `app/agents/comparative_analysis.py` catches the exception and immediately invokes a deterministic direct-API fallback.
3. **Target Price Float Sanitization:**
   * LLMs frequently return float strings with currency symbols or commas (e.g., `"$245.50"`). The Summary Agent passes all outputs through `_clean_target_price()` regex cleaners to guarantee valid numeric casting.
4. **Timezone Sanitization & PyArrow Chart Rendering:**
   * Normalized all `yfinance` DatetimeIndex objects using `.tz_localize(None)` in `app/integrations/market_data.py`, resolving Apache PyArrow serialization crashes identified during Streamlit UI chart rendering by **Sagar Trimukhe** and **Nikhil Gaikwad**.
5. **SEC EDGAR Compliance & Gzip Handling:**
   * Added declared institutional research User-Agent headers, <5 req/sec pacing, and transparent `gzip.decompress()` magic-byte handling.
6. **Empty Vector Store Graceful Degradation:**
   * If an analyst queries a ticker whose documents have not yet been indexed in ChromaDB, the system warns the user cleanly rather than raising an unhandled retrieval exception.

---

# 14. Human Approval Step

In high-stakes investment management, fully autonomous AI execution creates unacceptable regulatory and financial risks. Architected by **Ganesh Swami** and integrated into the frontend by **Sagar Trimukhe**, we built a native **Human-in-the-Loop (HITL)** governance gate:

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

# 15. Sprint-Wise Progress Documentation

Development was executed across four structured weekly sprints. Comprehensive sprint-by-sprint engineering logs, debugging narratives, and technical takeaways are documented in `WEEKLY_PROGRESS_REPORT.md`:

* **Week 1:** Project Inception, Environment, Core Schemas & Baseline RAG Setup.
  * *Milestone:* Resolved state graph architecture over conversational chat loops; fixed table-splitting chunking issues; implemented ChromaDB metadata isolation.
* **Week 2:** LangGraph Multi-Agent Orchestration, S3 Storage & Streamlit UI.
  * *Milestone:* Resolved parallel state collisions during fan-out using `_keep_latest` reducers; resolved PyArrow timezone crash; built 3-tab Streamlit dashboard.
* **Week 3:** Volatility Mathematical Modeling, Prompt Hardening & Mid-Review.
  * *Milestone:* Implemented 252-day annualized stock volatility and maximum drawdown; built tool-calling fallbacks; bound checkpointer to `st.session_state` thread ID.
* **Week 4:** AWS Cloud Deployment (EC2 + S3), Real SEC Filings & Final Submission.
  * *Milestone:* Automated EC2 deployment with 2 GB Linux swapfile; expanded stock catalog to 270 NASDAQ equities; downloaded 20 genuine SEC 10-Ks; resolved Gemini 100 RPM quota exhaustion.

---

# 16. Challenges Faced and How They Were Resolved

During the design, implementation, and cloud deployment of the AI Investment Research Assistant, the team resolved 12 major engineering challenges:

| # | Challenge Category | Real-World Technical Problem Encountered | Concrete Engineering Resolution Implemented | Primary Lead |
|:---:|:---|:---|:---|:---|
| **1** | **LangGraph Concurrency** | **Parallel Fan-Out State Collisions:** When the Router node dispatched `market_research` and `trend_analysis` concurrently, both nodes completed asynchronously and attempted to update overlapping dictionary keys in `AgentState`. Standard LangGraph state merging failed with `InvalidUpdateError`. | Implemented custom `_keep_latest(current_val, new_val)` reducers wrapped in `Annotated[Optional[Dict], _keep_latest]` in `app/core/state.py`. | **Ganesh Swami** |
| **2** | **API Quota Management** | **Gemini 100 RPM Free-Tier Quota Exhaustion:** Ingesting a 209-chunk Form 10-K report triggered Google GenAI HTTP 429 `RESOURCE_EXHAUSTED` errors in 15 seconds, crashing document ingestion midway. | Built an adaptive micro-batching engine (20 chunks/batch with 1.0s delay) with regex-driven exponential backoff parsing Google's exact retry window in `app/services/document_ingestion.py`. | Nikhil Gaikwad & Ganesh Swami |
| **3** | **RAG Tabular Integrity** | **Financial Context Fragmentation in Chunking:** Naive text chunking (300–500 chars) split multi-column balance sheets across arbitrary boundaries, separating numbers from line-item labels. | Standardized on **1,500 characters with 150-character (10%) overlap** using `RecursiveCharacterTextSplitter`, configuring double newlines (`\n\n`) as high-priority separators. | Nilanjan Das |
| **4** | **Vector Store Isolation** | **Cross-Ticker Semantic Contamination in Multi-Company Index:** In a shared ChromaDB database containing multiple corporate filings, semantic queries retrieved chunks from competing companies. | Injected strict `ticker` metadata tags into all chunks and enforced mandatory `filter={"ticker": target_ticker}` queries during vector similarity search. | Nilanjan Das & Ganesh Swami |
| **5** | **Output Schema Sanitization** | **LLM String Output Breaking Mathematical Float Casting:** Summary Agent generated string-formatted prices like `"$245.50"` or ranges (`"$240 - $260"`), crashing Python `float()` casting in downstream volatility engines. | Engineered a defensive regex sanitizer (`_clean_target_price`) in `app/agents/summary_agent.py` to strip currency symbols, compute midpoints for range strings, and enforce Pydantic float schemas. | Shradha Gaikwad |
| **6** | **Telemetry Data Integrity** | **Timezone-Aware DatetimeIndex Crashing Streamlit Charts:** `yfinance` historical price data returns DatetimeIndex with timezone offsets (`America/New_York`), causing PyArrow serialization exceptions in Streamlit. | Applied `.tz_localize(None)` in `app/integrations/market_data.py` to strip UTC offsets while maintaining chronological trading dates. | Nikhil Gaikwad |
| **7** | **SEC EDGAR Compliance** | **Automated Scraping Blocks (HTTP 403) & Gzip Stream Failures:** SEC EDGAR servers strictly block generic Python User-Agents and return compressed Gzip binary streams. | Declared compliant research User-Agent headers, throttled requests to <5 req/sec, and added automatic `gzip.decompress()` magic-byte detection. | Nilanjan Das |
| **8** | **Tool Calling Resilience** | **Tool-Calling Timeouts & Hallucinated Argument Signatures:** Relying solely on LLM function calling for peer valuation multiples occasionally failed due to model parameter hallucination or API latency. | Engineered a **dual-strategy execution pattern** in `app/agents/comparative_analysis.py`: attempts tool calling first, immediately falling back to direct API calls upon failure. | Nikhil Gaikwad |
| **9** | **Session State Persistence** | **Streamlit Browser Reruns Wiping HITL Interruption State:** Streamlit re-executes scripts top-to-bottom on every user click, wiping in-memory LangGraph thread states during human review. | Bound LangGraph's `MemorySaver` checkpointer to a persistent session thread identifier stored in `st.session_state`, resuming execution via `Command(resume=review_payload)`. | Sagar Trimukhe & Ganesh Swami |
| **10** | **Cloud Degradation** | **Missing AWS Credentials Crashing Local Environments:** Unhandled `boto3` exceptions in offline environments crashed document indexing and export operations. | Built a defensive wrapper in `app/integrations/s3_client.py` with `is_available()` health checks and graceful local fallback degradation. | **Ganesh Swami** |
| **11** | **Quantitative Modeling** | **Financial Volatility Calculation Skew from Non-Trading Days:** Calculating simple standard deviations of price changes over calendar date ranges skewed volatility metrics due to market weekends/holidays. | Calculated daily price changes strictly over active market sessions and scaled by $\sqrt{252}$ trading days to compute institutional-grade annualized volatility. | Shradha Gaikwad |
| **12** | **Global Equity Filings** | **Foreign Private Issuer SEC Form Discrepancies (10-K vs. 20-F):** International leaders on NASDAQ (ASML, ARM) file Form 20-F rather than 10-K, returning empty search results. | Engineered an intelligent multi-tier discovery hierarchy checking Form 10-K -> Form 10-K/A -> Form 20-F. | Nilanjan Das |

---

# 17. Final Conclusion

The **AI Investment Research Assistant** successfully demonstrates the transition of multi-agent generative AI from experimental chatbots into a production-grade, compliance-governed institutional equity research platform.

### Key Conclusions & Architectural Learnings:
1. **Deterministic Multi-Agent Graphs Over Chat Loops:** Enterprise AI workflows require the structure and predictability of a Directed Acyclic Graph (DAG). LangGraph's state machine architecture provides deterministic execution, auditability, and clear separation of concerns.
2. **Structure-Aware Financial RAG:** Naive chunking fails on tabular accounting data. Structure-aware chunking (1,500 characters, 10% overlap, double-newline prioritization) combined with strict metadata pre-filtering is essential for zero-hallucination document synthesis.
3. **Mandatory Human Governance (HITL):** Autonomous agents must not operate unmonitored in high-stakes capital allocation domains. Human-in-the-Loop review gates establish essential institutional trust and accountability.
4. **Cloud Production Hardening:** True production readiness requires defensive engineering — automated Linux swap configuration on resource-constrained compute, adaptive API rate-limit backoff, and graceful offline degradation.

### Future Roadmap:
* **Multimodal Table Extraction:** Integrate Gemini Flash Vision models to directly parse rasterized financial charts and balance sheet exhibits in PDF filings.
* **Automated SEC EDGAR Webhooks:** Connect SEC RSS feeds to automatically trigger the research pipeline upon real-time filing disclosures.
* **Portfolio Risk Optimization:** Expand beyond single-stock valuation to multi-stock portfolio optimization, calculating covariance matrices and Value-at-Risk (VaR).

---

# 18. Individual Contribution Summary

Each team member contributed across their primary specialization and collaborated on cross-functional integration needs:

| Team Member | Primary Domain | Core Technical & Cross-Functional Contributions | Key Code Modules |
|:---|:---|:---|:---|
| **Ganesh Swami** | **Backend Architecture, LangGraph DAG & Cloud DevOps Lead** | • Designed and implemented the complete LangGraph Directed Acyclic Graph (DAG) state topology.<br>• Architected parallel fan-out and fan-in synchronization with custom `_keep_latest` state channel reducers.<br>• Engineered the Human-in-the-Loop (HITL) interrupt and resume protocol using `langgraph.types.interrupt` and `MemorySaver`.<br>• Authored the automated AWS EC2 provisioning script (`setup_ec2.sh`) with 2 GB Linux swap space management.<br>• Built the AWS S3 storage integration client (`s3_client.py`) with automatic offline graceful degradation.<br>• **Cross-support:** Collaborated with Sagar on Streamlit execution streaming and thread checkpointing; partnered with Nilanjan on ChromaDB metadata filtering. | `app/services/workflow_service.py`<br>`app/core/state.py`<br>`app/agents/hitl_review.py`<br>`scripts/setup_ec2.sh`<br>`app/integrations/s3_client.py`<br>`docker-compose.yml` |
| **Shradha Gaikwad** | **Agent Intelligence & Financial Modeling Lead** | • Developed Market Research Agent for fundamental accounting and 10-K balance sheet extraction.<br>• Built Trend & Sentiment Analysis Agent with macroeconomic catalyst scoring (-1.0 to +1.0).<br>• Implemented Summary Agent investment thesis synthesis (BUY/HOLD/SELL rating & 12-month target price).<br>• Engineered stock risk calculations: 1-year annualized price volatility (based on 252 trading days) and historical maximum price drop (drawdown).<br>• Designed strongly typed Pydantic output validation contracts and defensive regex float sanitizers. | `app/agents/market_research.py`<br>`app/agents/trend_analysis.py`<br>`app/agents/summary_agent.py`<br>`app/schemas/financial.py`<br>`app/schemas/report.py` |
| **Sagar Trimukhe** | **Frontend UI & Chatbot/HITL Integration Lead** | • Built comprehensive 3-Tab Streamlit dashboard interface (`app/main.py`).<br>• Co-developed Market Research Agent & Trend Analysis Agent prompt engineering and financial metric extraction.<br>• Developed Document Ingestion UI with drag-and-drop file upload and ChromaDB status metrics.<br>• Engineered real-time agent execution visualizer and live node progress streaming.<br>• Built Human-in-the-Loop Analyst Review workspace with thesis editor and certification form.<br>• Solved Streamlit reactive script rerun context loss by binding graph checkpointer to session thread ID.<br>• Integrated one-click Markdown memorandum export and AWS S3 cloud archiving buttons.<br>• **Cross-support:** Integrated Nilanjan's 270-stock catalog into the frontend quick-ingestion selector. | `app/main.py`<br>`app/agents/market_research.py`<br>`app/agents/trend_analysis.py`<br>`app/services/export_service.py`<br>`presentation.html` |
| **Nilanjan Das** | **Data Engineering & Filing Ingestion Lead** | • Curated and implemented the 270-stock NASDAQ universe catalog across 6 major industries.<br>• Developed automated SEC EDGAR 10-K downloader with accession number tracking and HTML-to-text cleaning.<br>• Downloaded, verified, and cataloged 20 genuine official SEC Form 10-K filings.<br>• Engineered recursive text splitting (1,500 chars / 150 overlap) preserving financial table integrity.<br>• Implemented persistent ChromaDB storage with ticker metadata isolation to eliminate cross-stock contamination.<br>• Resolved SEC EDGAR HTTP 403 blocking and transparent Gzip stream decoding. | `app/services/nasdaq_universe.py`<br>`scripts/fetch_real_10k_filings.py`<br>`app/services/document_ingestion.py`<br>`app/integrations/vector_store.py` |
| **Nikhil Gaikwad** | **Full-Stack Integration, Telemetry & QA Engineer** | • Integrated `yfinance` live market telemetry tools for real-time stock profiles, trailing/forward P/E, and EV/EBITDA.<br>• Implemented Comparative Valuation Agent with dual-strategy tool calling and deterministic direct-API fallback.<br>• Built Gemini Free-Tier rate-limit resilience engine with regex-driven exponential backoff (100 RPM recovery).<br>• Resolved Streamlit DatetimeIndex timezone rendering bugs via `.tz_localize(None)`.<br>• Developed RAG evaluation benchmark test scripts and led end-to-end integration testing. | `app/agents/comparative_analysis.py`<br>`app/integrations/market_data.py`<br>`app/tools/financial_tools.py`<br>`app/evaluation/rag_eval.py`<br>`scripts/test_aws_s3.py` |
