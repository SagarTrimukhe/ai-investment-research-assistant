# Sprint-Wise Weekly Progress Report
## Capstone Project: AI Investment Research Assistant (Theme 15 - Finance Domain)
**Program:** Advanced PG Certification in AI Engineering on Cloud and AIOps  
**Institution:** IIT Roorkee, powered by Futurense  
**Cohort Duration:** 08 September 2026 – 09 October 2026  
**Submission Deadline:** 09 October 2026  

### Team Members
1. **Ganesh Swami** — Backend & Multi-Agent Architecture Lead
2. **Shradha Gaikwad** — Backend, Financial Agents & Quantitative Modeling Lead
3. **Sagar Trimukhe** — Frontend Dashboard & Chatbot/HITL Integration Lead
4. **Nilanjan Das** — Data Engineering, SEC Filings & Vector RAG Pipeline Lead
5. **Nikhil Gaikwad** — Full-Stack Integration, Tooling & Quality Assurance Engineer

---

## Executive Overview
This document tracks sprint-by-sprint development progress, technical deliverables, architectural milestones, engineering roadblocks, debugging experiences, and individual contributions for the **AI Investment Research Assistant** across the capstone lifecycle.

Unlike a high-level summary, this report documents the **authentic student engineering journey**: the architectural dead-ends we encountered, the bugs that broke our local environments, the debugging steps taken, and the technical insights we gained as we transitioned from theoretical concepts to a production-grade multi-agent system.

```
+--------------------------------------------------------------------------------------------------+
|                                    COHORT SPRINT ROADMAP                                         |
+--------------------------------------------------------------------------------------------------+
|  Week 1 (08 Sep - 15 Sep)  : Project Inception, Environment, Core Schemas & Baseline RAG Setup   |
|  Week 2 (16 Sep - 23 Sep)  : LangGraph Multi-Agent Orchestration, S3 Storage & Streamlit UI      |
|  Week 3 (24 Sep - 01 Oct)  : Volatility Mathematical Modeling, Prompt Hardening & Mid-Review     |
|  Week 4 (02 Oct - 09 Oct)  : AWS Cloud Deployment (EC2 + S3), Real SEC Filings & Final Submission |
+--------------------------------------------------------------------------------------------------+
```

---

## Week 1 Progress: Project Inception, Environment, Core Schemas & Baseline RAG Setup
**Timeline:** 08 September 2026 – 15 September 2026  
**Status:** Completed  

### 1. Objectives & Scope
* Review domain problem statements and finalize **Theme 15: AI Investment Research Assistant** in the Finance domain.
* Identify target user personas (buy-side and sell-side equity analysts, portfolio managers) and quantify the fundamental bottlenecks in processing SEC Form 10-K and 10-Q filings.
* Set up reproducible local development scaffolding: Python 3.10 virtual environments, Docker containerization, Git repository, and CI/dependency specifications.
* Establish baseline connectivity with Google Gemini (`gemini-2.5-flash` / `gemini-1.5-flash`), ChromaDB vector store, and `yfinance` market data APIs.
* Define foundational Pydantic schemas, typed state models, and initial RAG document chunking and ingestion pipelines.

### 2. Activities & Key Deliverables
* **Project Scoping & Domain Research (08–09 Sep) — *All Members*:**
  * Reviewed sample corporate filings (Apple FY2023 10-K, Meta, Microsoft). Analyzed that institutional analysts spend over 70% of their working hours manually scanning 60–150 page documents, extracting balance sheet line items, and computing historical valuation multiples before drafting investment recommendations.
  * Defined core product value proposition: an autonomous multi-agent pipeline that ingests raw SEC filings, extracts quantitative metrics, evaluates market sentiment, benchmarks peers, and generates an auditable investment memorandum with Human-in-the-Loop oversight.
* **Environment Scaffolding & Container Scaffolding (09–10 Sep) — *Ganesh Swami & Shradha Gaikwad*:**
  * Created project repository structure adhering to clean architecture principles (`app/agents`, `app/core`, `app/integrations`, `app/schemas`, `app/services`, `app/tools`).
  * Built [`Dockerfile`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/Dockerfile) and [`docker-compose.yml`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/docker-compose.yml) ensuring portability across developer macOS/Linux machines and eventual AWS EC2 deployment.
  * Implemented centralized configuration management in [`app/core/config.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/core/config.py) using `pydantic-settings` to securely load API credentials (`GEMINI_API_KEY`, AWS credentials, vector store paths) with fallback defaults.
* **Data Ingestion & Vector Storage Pipeline (11–13 Sep) — *Nilanjan Das & Nikhil Gaikwad*:**
  * Implemented [`app/services/document_ingestion.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/services/document_ingestion.py) supporting PDF extraction (`pypdf`) and raw TXT document processing.
  * Configured ChromaDB persistent storage client ([`app/integrations/vector_store.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/integrations/vector_store.py)) with local directory persistence under `data/chroma_db/`.
  * Integrated `yfinance` in [`app/integrations/market_data.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/integrations/market_data.py) to extract live company overview metrics (trailing P/E, forward P/E, market cap, 52-week price range).
* **Initial Agent Nodes & Typed Schemas (14–15 Sep) — *Shradha Gaikwad & Ganesh Swami*:**
  * Defined strongly typed global state schema [`AgentState`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/core/state.py) as a `TypedDict` capturing pipeline inputs, intermediate agent payloads, risk metrics, and review statuses.
  * Authored initial agent prompts for the **Market Research Agent** ([`app/agents/market_research.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/market_research.py)) to parse financial statements and the **Trend Analysis Agent** ([`app/agents/trend_analysis.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/trend_analysis.py)) to score market sentiment from -1.0 to +1.0.

### 3. Roadblocks & Technical Challenges (Sprint 1)

#### 🔴 Roadblock 1.1: Conversational Chat Loops vs. Deterministic State Machines
* **How We Hit the Issue:**  
  In our first prototype, we attempted to build a multi-agent system using open conversational loops (similar to basic AutoGen or conversational chat loops where agents exchange free-form text messages). When Ganesh and Shradha ran the prototype, the Market Research agent and Trend agent repeatedly drifted into circular debates about macro risks, hallucinated arbitrary next steps, or skipped fundamental balance sheet analysis altogether. The pipeline lacked determinism, execution order was unpredictable, and there was no way to enforce audit gates.
* **Debugging & Investigation:**  
  We realized that while conversational loops work for brainstorming chatbots, financial equity research is a disciplined, regulatory-constrained workflow. In equity research, step 1 (sanitizing tickers) must precede step 2 (parallel data retrieval), which must complete before step 3 (synthesis) and step 4 (compliance sign-off).
* **Engineering Resolution:**  
  We abandoned unstructured chat loops and standardized on **LangGraph** using a strictly typed Directed Acyclic Graph (DAG) state topology. We defined state as a centralized `AgentState` schema, giving every node explicit read/write boundaries and making the entire pipeline deterministic, auditable, and replayable.
* **Student Takeaway & Learning:**  
  *We learned that "multi-agent" in enterprise systems does not mean agents chatting socially with each other. It means a formal distributed state machine where specialized components perform isolated tasks governed by strict input/output contracts.*

#### 🔴 Roadblock 1.2: The "Split Table" RAG Chunking Crisis
* **How We Hit the Issue:**  
  Nilanjan ingested the Apple 10-K filing using standard recursive chunking with a 400-character window and 50-character overlap. When we tested semantic queries like `"What was Apple's total net sales in 2023?"`, ChromaDB returned chunks containing lone figures like `"$383,285"` and `"$394,328"` completely divorced from their column labels ("Products", "Services", "Total Net Sales"). As a result, Gemini hallucinated that Apple's total sales were actually its R&D expenses!
* **Debugging & Investigation:**  
  Inspecting the raw chunked text revealed that naive character splitting sliced through the middle of markdown and ASCII accounting tables. A balance sheet table spanning 800 characters was split across three separate chunks, destroying row-column contextual associations.
* **Engineering Resolution:**  
  Nilanjan experimented with chunk sizes from 300 to 2,000 characters. We standardized on **1,500 characters with 150-character (10%) overlap** using `RecursiveCharacterTextSplitter`. Critically, we reordered the text splitting separators to prioritize double newlines (`\n\n`), single newlines (`\n`), and table pipes (`|`) before breaking on sentence periods or spaces. This preserved intact multi-line financial tables within individual chunks.
* **Student Takeaway & Learning:**  
  *We learned that chunking strategy cannot be treated as a generic hyperparameter. Financial documents have distinct structural syntax; preserving semantic table boundaries is 10x more important than raw embedding similarity scores.*

#### 🔴 Roadblock 1.3: Cross-Ticker Context Contamination in ChromaDB
* **How We Hit the Issue:**  
  During testing, we ingested both Apple (`AAPL`) and Meta (`META`) filings into our local ChromaDB instance. When asking the pipeline to research `"revenue growth drivers"`, the retrieval engine pulled chunks discussing Meta's digital advertising rebound alongside Apple's iPhone gross margins. The resulting summary synthesized a bizarre hybrid company that sold iPhones while generating ad revenue on Instagram!
* **Debugging & Investigation:**  
  Because semantic embeddings map meaning rather than exact entity names, vector similarity between "quarterly revenue increase" in Apple's filing and "quarterly advertising revenue growth" in Meta's filing was extremely high (~0.84 cosine similarity). Without explicit namespace isolation, ChromaDB retrieved chunks based solely on keyword semantic proximity.
* **Engineering Resolution:**  
  Nilanjan re-engineered the ingestion pipeline to inject strict metadata into every chunk: `{"ticker": target_ticker.upper(), "source": filename, "chunk_id": idx}`. In [`app/integrations/vector_store.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/integrations/vector_store.py), we enforced mandatory metadata filtering in all similarity searches: `filter={"ticker": target_ticker}`.
* **Student Takeaway & Learning:**  
  *We learned that pure semantic search is dangerous in multi-tenant or multi-entity systems. Hybrid retrieval—combining hard metadata pre-filtering with semantic vector ranking—is essential to prevent context pollution.*

---

## Week 2 Progress: LangGraph Multi-Agent Orchestration, S3 Storage & Streamlit UI
**Timeline:** 16 September 2026 – 23 September 2026  
**Status:** Completed  

### 1. Objectives & Scope
* Implement remaining core agents: **Router Node**, **Comparative Valuation Agent**, **Summary Agent**, and **Human-in-the-Loop Review Node**.
* Compile the complete LangGraph state graph with persistent checkpointing to support parallel fan-out and pause/resume execution.
* Build cloud object storage integration with AWS S3 for automated research memorandum archiving.
* Develop an interactive 3-tab frontend dashboard using Streamlit for document ingestion, real-time agent execution streaming, and analyst review.
* Resolve concurrency race conditions and data serialization bugs encountered during full-stack integration.

### 2. Activities & Key Deliverables
* **Agent Implementation & Review Logic (16–17 Sep) — *Shradha Gaikwad & Ganesh Swami*:**
  * Developed the **Router Node** ([`app/agents/router.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/router.py)) to sanitize ticker symbols, validate against supported NASDAQ universe, and assign sector-specific benchmark peers (e.g., assigning MSFT as peer benchmark for AAPL, AMD for NVDA).
  * Developed the **Comparative Valuation Agent** ([`app/agents/comparative_analysis.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/comparative_analysis.py)) to compare valuation multiples (Trailing P/E, Forward P/E, Price-to-Sales) against peer competitors.
  * Developed the **Summary Agent** ([`app/agents/summary_agent.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/summary_agent.py)) to synthesize financial metrics, qualitative risks, and market sentiment into a structured investment thesis with BUY/HOLD/SELL ratings.
  * Implemented Human-in-the-Loop review gate ([`app/agents/hitl_review.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/hitl_review.py)) utilizing `langgraph.types.interrupt()`.
* **State Graph Assembly & Checkpointing (18–19 Sep) — *Ganesh Swami*:**
  * Wired all nodes in [`app/services/workflow_service.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/services/workflow_service.py) creating a Directed Acyclic Graph:
    `router -> [market_research || trend_analysis] -> comparative_analysis -> summary -> hitl_review -> END`.
  * Integrated LangGraph's `MemorySaver` checkpointer to maintain thread state across async execution boundaries.
* **AWS S3 Storage Client & Exporter (20–21 Sep) — *Nikhil Gaikwad & Ganesh Swami*:**
  * Built [`app/integrations/s3_client.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/integrations/s3_client.py) using `boto3` to upload raw filings and finalized research memorandums to S3 bucket `ai-investment-research-repo`.
  * Implemented Markdown export service in [`app/services/export_service.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/services/export_service.py) generating formatted institutional reports.
* **Streamlit UI Development (22–23 Sep) — *Sagar Trimukhe & Nikhil Gaikwad*:**
  * Built 3-tab frontend dashboard in [`app/main.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/main.py):
    * **Tab 1 (Document Ingestion):** File uploader supporting PDF/TXT, ticker detector, and live ChromaDB collection statistics.
    * **Tab 2 (Research & Analysis):** Real-time stock profile header, interactive historical stock chart, and live execution progress log.
    * **Tab 3 (Analyst Review Workspace):** HITL form with editable recommendation, target price adjustment, compliance notes, and S3 export trigger.

### 3. Roadblocks & Technical Challenges (Sprint 2)

#### 🔴 Roadblock 2.1: Parallel State Collision (`InvalidUpdateError`) During Graph Fan-Out
* **How We Hit the Issue:**  
  To speed up execution, Ganesh designed the graph so that after the Router node, `market_research` and `trend_analysis` ran concurrently in parallel. However, the moment both nodes finished and attempted to merge their updates back into the centralized `AgentState`, LangGraph crashed with:
  `langgraph.errors.InvalidUpdateError: At key '__root__': received conflicting concurrent updates for state keys`.
* **Debugging & Investigation:**  
  We learned that LangGraph's default state behavior is overwrite-based. When two child nodes execute simultaneously in parallel branches, they attempt to overwrite the parent state dictionary concurrently, creating an unresolvable write conflict.
* **Engineering Resolution:**  
  Ganesh researched LangGraph's reducer architecture and discovered `typing.Annotated` channel reducers. In [`app/core/state.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/core/state.py), we defined a custom merge function:
  ```python
  def _keep_latest(current: Any, update: Any) -> Any:
      return update if update is not None else current
  ```
  We wrapped state attributes in `Annotated[Optional[Dict[str, Any]], _keep_latest]`. This instructed the LangGraph engine how to safely combine asynchronous updates from multiple branches without raising concurrency exceptions.
* **Student Takeaway & Learning:**  
  *We gained firsthand experience in distributed state management. Parallelism in AI agent workflows requires explicit merge strategies just like concurrent threads in operating systems.*

#### 🔴 Roadblock 2.2: PyArrow Timezone Serialization Crash in Streamlit Charts
* **How We Hit the Issue:**  
  Sagar connected `yfinance` historical price data to Streamlit's `st.line_chart()`. For several stocks, clicking "Run Research" caused the entire Streamlit frontend to crash with an unhandled exception:
  `pyarrow.lib.ArrowInvalid: Cannot mix tz-aware and tz-naive timestamps in arrow table`.
* **Debugging & Investigation:**  
  Nikhil inspected the DataFrame returned by `ticker.history(period="1y")`. Depending on whether yfinance returned market data from NYSE or NASDAQ during active trading hours, the DatetimeIndex included timezone offset strings (e.g., `Timestamp('2026-09-22 09:30:00-0400', tz='America/New_York')`). Streamlit uses Apache PyArrow under the hood for high-speed table rendering, and PyArrow strictly rejects DataFrames containing timezone-aware timestamps when converting to Apache Arrow tables.
* **Engineering Resolution:**  
  In [`app/integrations/market_data.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/integrations/market_data.py), Nikhil added defensive timestamp normalization:
  ```python
  if hist.index.tz is not None:
      hist.index = hist.index.tz_localize(None)
  ```
  This cleanly stripped UTC offsets while preserving the exact chronological trading dates, allowing PyArrow and Streamlit to render smoothly across all equities.
* **Student Takeaway & Learning:**  
  *We learned that third-party financial data APIs return subtle data types that can break frontend rendering engines. Data cleaning at the API ingestion boundary is critical before passing data to UI components.*

#### 🔴 Roadblock 2.3: String Hallucinations in Quantitative Target Price Outputs
* **How We Hit the Issue:**  
  In early end-to-end runs, Shradha's Summary Agent outputted target prices formatted in natural language: e.g., `"$250.00"`, `"Approximately $245"`, or `"Range: $240 - $260"`. Downstream, when the mathematical risk module attempted to compute expected percentage upside:
  `upside = ((target_price - current_price) / current_price) * 100`
  the application threw `TypeError: unsupported operand type(s) for -: 'str' and 'float'`.
* **Debugging & Investigation:**  
  Even though our prompt instructed Gemini to "return a numeric target price", LLMs are probabilistic text generators and frequently add dollar symbols, commas, or estimated ranges when discussing monetary amounts.
* **Engineering Resolution:**  
  Shradha implemented a dual defense:
  1. Updated the Pydantic schema in [`app/schemas/report.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/schemas/report.py) to explicitly enforce `target_price: float`.
  2. Built a defensive regex cleaner `_clean_target_price()` in [`app/agents/summary_agent.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/summary_agent.py) that strips currency signs (`$`, `€`, `,`), detects range expressions (e.g., `"240 - 260"`), computes the mathematical midpoint, and returns a sanitized `float`.
* **Student Takeaway & Learning:**  
  *We realized that LLM output guarantees cannot rely on prompt instructions alone. Production AI systems require deterministic parsing and regex sanity checks before handing data over to quantitative code.*

---

## Week 3 Progress: Volatility Mathematical Modeling, Prompt Hardening & Mid-Review
**Timeline:** 24 September 2026 – 01 October 2026  
**Status:** Completed  

### 1. Objectives & Scope
* Implement quantitative financial risk metrics: **1-year Annualized Price Volatility** and **Historical Maximum Drawdown**.
* Conduct end-to-end multi-agent evaluation on diverse corporate profiles (Apple, NVIDIA, Meta, Infosys).
* Benchmark RAG retrieval precision and optimize prompt schemas to eliminate JSON hallucinations.
* Prepare, rehearse, and present the mid-capstone project review demonstration to the faculty evaluation panel.

### 2. Activities & Key Deliverables
* **Quantitative Risk Engine Integration (24–26 Sep) — *Shradha Gaikwad*:**
  * Implemented mathematical risk algorithms in [`app/agents/summary_agent.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/summary_agent.py):
    * Calculated daily percentage logarithmic returns $r_t = \ln(P_t / P_{t-1})$.
    * Computed **Annualized Volatility** scaled by the trading calendar year: $\sigma_{\text{ann}} = \sigma_{\text{daily}} \times \sqrt{252} \times 100\%$.
    * Computed **Rolling Maximum Drawdown**: tracking peak-to-trough price declines: $\text{MDD} = \min\left(\frac{P_t - \text{Peak}_t}{\text{Peak}_t}\right) \times 100\%$.
* **RAG Retrieval Validation & Isolation Testing (27–28 Sep) — *Nilanjan Das*:**
  * Benchmarked retrieval precision across heterogeneous corporate reports: Apple 10-K, Meta Earnings Presentation Q2-2026, and Infosys Fact Sheet.
  * Verified that vector search with ticker metadata filtering achieved 100% isolation with zero cross-company chunk leakage.
* **Prompt Hardening & Tool Calling Fallbacks (29–30 Sep) — *Nikhil Gaikwad & Shradha Gaikwad*:**
  * Hardened Gemini system instructions with explicit JSON output requirements, reducing malformed JSON responses to 0%.
  * Implemented deterministic fallback in Comparative Valuation Agent when Gemini function calling faced network latency spikes.
* **Mid-Cohort Demonstration & Feedback (01 Oct) — *Sagar Trimukhe & Ganesh Swami*:**
  * Successfully demonstrated live end-to-end execution of the research pipeline to the evaluation committee.
  * Demonstrated document upload, parallel agent execution, real-time logging, and analyst sign-off with memorandum generation.

### 3. Roadblocks & Technical Challenges (Sprint 3)

#### 🔴 Roadblock 3.1: Volatility Calculation Skew from Calendar vs. Trading Days
* **How We Hit the Issue:**  
  When Shradha initially implemented the volatility calculation, she computed standard deviation across all calendar dates (365 days). When testing against known market benchmarks (e.g., Apple's published 1-year historical volatility of ~18–20%), our system computed an artificially depressed volatility of ~14.8%.
* **Debugging & Investigation:**  
  Researching quantitative finance literature revealed our error: financial markets are closed on weekends (~104 days) and federal holidays (~9 days). Using calendar days or filling weekend gaps with zero-change prices artificially diluted daily price variance. Standard quantitative practice uses **252 active trading days**.
* **Engineering Resolution:**  
  Shradha revised the mathematical logic: daily returns are calculated strictly over sequential active market sessions using `pct_change().dropna()`. The daily standard deviation is then multiplied by $\sqrt{252}$, yielding an exact match with institutional market metrics (e.g., AAPL calculated at 19.4% annualized volatility).
* **Student Takeaway & Learning:**  
  *We learned that applying mathematics to real-world domain data requires respecting domain-specific conventions. In quantitative finance, the difference between calendar days and trading days fundamentally alters risk assessments.*

#### 🔴 Roadblock 3.2: Tool-Calling Timeouts During Peer Benchmarking
* **How We Hit the Issue:**  
  In the Comparative Valuation Agent, we instructed Gemini to call live market tools for both the target stock and its benchmark competitor in a single turn. When testing with NVIDIA (`NVDA`) and AMD (`AMD`), Gemini occasionally failed to trigger the tool call, generated hallucinated parameter names, or timed out after 30 seconds due to sequential API latency.
* **Debugging & Investigation:**  
  Relying exclusively on the LLM to decide when and how to call tools introduced a single point of failure. If the LLM suffered a momentary hallucination or the external financial API experienced network lag, the entire downstream pipeline stalled.
* **Engineering Resolution:**  
  Nikhil implemented a resilient **dual-strategy execution pattern** in [`app/agents/comparative_analysis.py`](file:///Users/ganesh-test/Documents/ai-investment-research-assistant/app/agents/comparative_analysis.py):
  1. The agent first attempts LLM tool calling.
  2. If the tool call fails, times out, or returns incomplete data, the system instantly catches the exception and falls back to deterministic direct API fetching via `market_data.get_stock_overview()`.
* **Student Takeaway & Learning:**  
  *We learned defensive engineering for AI agents: never rely solely on an LLM for mission-critical data fetching. Always implement deterministic code fallbacks to guarantee pipeline resilience.*

#### 🔴 Roadblock 3.3: Streamlit Script Rerun Wiping HITL Interruption Context
* **How We Hit the Issue:**  
  When testing the Human-in-the-Loop review feature, LangGraph paused execution as expected using `interrupt()`. The analyst review form appeared in Streamlit Tab 3. However, the moment the user entered comments and clicked "Approve & Generate Memorandum", Streamlit re-executed `main.py` from line 1. Because the session state was not properly synchronized with LangGraph's in-memory thread, the graph lost its position and restarted the entire analysis from scratch!
* **Debugging & Investigation:**  
  Sagar studied Streamlit's execution model. Unlike traditional desktop or single-page web applications that maintain event loops, Streamlit reruns the entire Python script upon every user interaction. When the script reran, a new thread ID was generated, decoupling the UI from the paused LangGraph execution thread.
* **Engineering Resolution:**  
  Sagar bound LangGraph's `MemorySaver` checkpointer to a persistent session thread ID stored in `st.session_state["thread_id"]`. When the analyst submits the approval form, the application retrieves the existing thread ID and calls:
  `workflow.stream(Command(resume=review_payload), config={"configurable": {"thread_id": thread_id}})`
  This allowed LangGraph to resume cleanly from the exact interrupt node without re-executing completed predecessor nodes.
* **Student Takeaway & Learning:**  
  *We learned how to reconcile reactive, stateless frontend frameworks like Streamlit with stateful orchestration frameworks like LangGraph by anchoring execution context to persistent session keys.*

---

