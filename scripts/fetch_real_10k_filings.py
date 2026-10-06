#!/usr/bin/env python3
"""
Download REAL Official SEC 10-K Filing Documents from EDGAR.
Pulls the actual publicly filed annual reports (not generated/templated),
extracts clean text from the HTML filings, and saves them locally.

These are genuine, official SEC filings — the same documents available
on https://www.sec.gov/cgi-bin/browse-edgar

Stored in data/nasdaq_reports/ (Git-ignored) for offline testing.
"""
import gzip
import io

import os
import sys
import json
import re
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Tuple

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "nasdaq_reports"))

SEC_HEADERS = {
    "User-Agent": "AcademicResearchInvestmentAssistant/1.0 (academic_research_agent@university.edu)",
}


def _read_response(resp) -> bytes:
    """Read HTTP response, handling gzip compression transparently."""
    raw = resp.read()
    if resp.headers.get("Content-Encoding") == "gzip" or raw[:2] == b'\x1f\x8b':
        return gzip.decompress(raw)
    return raw

# 20 key stocks to download real 10-K filings for
# chosen for a diverse mix across sectors with reliable EDGAR filings
KEY_STOCKS = [
    ("AAPL", 320193, "Apple Inc."),
    ("MSFT", 789019, "Microsoft Corporation"),
    ("NVDA", 1045810, "NVIDIA Corporation"),
    ("AMZN", 1018724, "Amazon.com Inc."),
    ("GOOGL", 1652044, "Alphabet Inc."),
    ("META", 1326801, "Meta Platforms Inc."),
    ("TSLA", 1318605, "Tesla Inc."),
    ("NFLX", 1065280, "Netflix Inc."),
    ("AMD", 2488, "Advanced Micro Devices Inc."),
    ("INTC", 50863, "Intel Corporation"),
    ("CRM", 1108524, "Salesforce Inc."),
    ("ADBE", 796343, "Adobe Inc."),
    ("PYPL", 1633917, "PayPal Holdings Inc."),
    ("CSCO", 858877, "Cisco Systems Inc."),
    ("AMGN", 318154, "Amgen Inc."),
    ("COST", 909832, "Costco Wholesale Corp."),
    ("PEP", 77476, "PepsiCo Inc."),
    ("QCOM", 804328, "QUALCOMM Inc."),
    ("GILD", 882095, "Gilead Sciences Inc."),
    ("SBUX", 829224, "Starbucks Corporation"),
]


def find_latest_10k(cik: int) -> Optional[Tuple[str, str, str]]:
    """
    Query EDGAR submissions API to find the most recent 10-K filing.
    Returns (accession_number, primary_document, filing_date) or None.
    """
    cik_padded = str(cik).zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    req = urllib.request.Request(url, headers=SEC_HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = _read_response(resp)
            data = json.loads(raw.decode("utf-8"))
    except Exception as e:
        print(f"    [!] Failed to query submissions for CIK {cik}: {e}")
        return None

    filings = data.get("filings", {}).get("recent", {})
    forms = filings.get("form", [])
    accessions = filings.get("accessionNumber", [])
    primary_docs = filings.get("primaryDocument", [])
    dates = filings.get("filingDate", [])

    for i, form in enumerate(forms):
        if form == "10-K":
            return (accessions[i], primary_docs[i], dates[i])

    # fallback: try 10-K/A (amended)
    for i, form in enumerate(forms):
        if form == "10-K/A":
            return (accessions[i], primary_docs[i], dates[i])

    return None


def download_filing_html(cik: int, accession: str, primary_doc: str) -> Optional[str]:
    """Download the actual HTML filing document from EDGAR."""
    acc_no_dash = accession.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no_dash}/{primary_doc}"

    req = urllib.request.Request(url, headers=SEC_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = _read_response(resp)
            return raw.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"    [!] Failed to download filing: {e}")
        return None


def html_to_clean_text(html: str) -> str:
    """
    Convert SEC filing HTML to clean readable plain text.
    Handles inline XBRL, nested tables, and HTML entities.
    """
    # Insert newlines before/after block-level elements
    block_tags = ["</p>", "</div>", "</tr>", "</li>", "</h1>", "</h2>", "</h3>",
                  "</h4>", "</h5>", "</h6>", "</table>", "</section>", "<br>",
                  "<br/>", "<br />"]
    for tag in block_tags:
        html = html.replace(tag, tag + "\n")

    # Remove style, script, and comment blocks
    text = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # Remove ix:header (inline XBRL hidden header section)
    text = re.sub(r"<ix:header>.*?</ix:header>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Strip remaining HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode common HTML entities
    entity_map = {
        "&nbsp;": " ", "&amp;": "&", "&lt;": "<", "&gt;": ">",
        "&rsquo;": "'", "&lsquo;": "'", "&ldquo;": '"', "&rdquo;": '"',
        "&mdash;": "—", "&ndash;": "–", "&bull;": "•", "&middot;": "·",
        "&copy;": "©", "&reg;": "®", "&trade;": "™", "&apos;": "'",
        "&quot;": '"', "&hellip;": "…", "&times;": "×", "&divide;": "÷",
    }
    for entity, char in entity_map.items():
        text = text.replace(entity, char)
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))) if int(m.group(1)) < 65536 else "", text)
    text = re.sub(r"&#x([0-9a-fA-F]+);", lambda m: chr(int(m.group(1), 16)) if int(m.group(1), 16) < 65536 else "", text)

    # Clean whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Split lines and trim
    lines = [line.strip() for line in text.strip().splitlines()]

    # Skip XBRL metadata at the beginning — find where the real filing starts
    start_idx = 0
    for i, line in enumerate(lines):
        upper_line = line.upper()
        if ("FORM 10-K" in upper_line or
            "ANNUAL REPORT" in upper_line or
            "SECURITIES AND EXCHANGE COMMISSION" in upper_line or
            "WASHINGTON, D.C." in upper_line):
            start_idx = max(0, i - 1)
            break

    clean_lines = lines[start_idx:]

    # Remove purely empty lines at the start
    while clean_lines and not clean_lines[0]:
        clean_lines.pop(0)

    return "\n".join(clean_lines)


def process_stock(ticker: str, cik: int, name: str) -> dict:
    """Download and process a single stock's 10-K filing."""
    result = {
        "ticker": ticker,
        "name": name,
        "cik": cik,
        "status": "failed",
        "filing_date": None,
        "chars": 0,
        "lines": 0,
    }

    # Step 1: Find latest 10-K
    filing_info = find_latest_10k(cik)
    if not filing_info:
        print(f"  [{ticker}] No 10-K filing found on EDGAR")
        return result

    accession, primary_doc, filing_date = filing_info
    result["filing_date"] = filing_date
    print(f"  [{ticker}] Found 10-K filed {filing_date}: {primary_doc}")

    # Step 2: Download the HTML filing
    html = download_filing_html(cik, accession, primary_doc)
    if not html:
        return result

    # Step 3: Convert to clean text
    clean_text = html_to_clean_text(html)

    # Add a header for our pipeline
    header = f"""{'='*80}
OFFICIAL SEC FORM 10-K FILING — {name} ({ticker})
Downloaded from SEC EDGAR (https://www.sec.gov)
CIK: {str(cik).zfill(10)} | Accession: {accession} | Filed: {filing_date}
This is the GENUINE publicly filed annual report, not a generated summary.
{'='*80}

"""
    full_text = header + clean_text

    # Step 4: Save to file
    filename = f"{ticker}_10K_filing.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_text)

    result["status"] = "success"
    result["chars"] = len(full_text)
    result["lines"] = full_text.count("\n")
    result["filename"] = filename
    result["accession"] = accession

    return result


def main():
    print("=" * 70)
    print("  SEC EDGAR — Official 10-K Filing Downloader")
    print("  Downloading REAL publicly filed annual reports")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\nTarget: {len(KEY_STOCKS)} key stocks")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Source: SEC EDGAR (https://www.sec.gov)\n")

    results = []
    start_time = time.time()

    for i, (ticker, cik, name) in enumerate(KEY_STOCKS):
        print(f"[{i+1}/{len(KEY_STOCKS)}] Processing {ticker} ({name})...")
        res = process_stock(ticker, cik, name)
        results.append(res)

        # Respect SEC rate limits — 10 requests/second max
        # we do ~3 requests per stock, so pause between stocks
        if i < len(KEY_STOCKS) - 1:
            time.sleep(1.2)

    elapsed = time.time() - start_time
    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]

    print(f"\n{'='*70}")
    print(f"  RESULTS: {len(success)} succeeded, {len(failed)} failed ({elapsed:.1f}s)")
    print(f"{'='*70}")

    for r in success:
        print(f"  ✓ {r['ticker']:6s} | {r['name']:35s} | Filed {r['filing_date']} | {r['chars']:>8,} chars | {r['lines']:>5,} lines")

    if failed:
        print(f"\n  Failed:")
        for r in failed:
            print(f"  ✗ {r['ticker']:6s} | {r['name']}")

    # Save download manifest
    manifest_path = os.path.join(OUTPUT_DIR, "REAL_FILINGS_MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nManifest saved: {manifest_path}")


if __name__ == "__main__":
    main()
