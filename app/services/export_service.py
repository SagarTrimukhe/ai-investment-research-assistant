import os
import json


class ExportService:
    """Service to export research reports into readable formats."""

    def to_markdown(self, report_data: dict, output_path: str) -> str:
        """Export research report dictionary to a markdown file."""
        ticker = report_data.get("ticker", "STOCK")
        benchmark = report_data.get("benchmark", "PEER")
        draft = report_data.get("draft_thesis", {})

        rating = draft.get("rating", report_data.get("rating", "N/A"))
        target_price = draft.get("target_price", report_data.get("target_price", "N/A"))
        summary = draft.get("executive_summary", "")

        lines = [
            f"# Investment Research Report: {ticker}",
            f"**Benchmark Peer:** {benchmark}",
            f"**Rating:** {rating}",
            f"**Target Price:** ${target_price}",
            "",
            "## Executive Summary",
            summary if summary else "No summary provided.",
            "",
            "## Core Thesis Points",
        ]

        for pt in draft.get("thesis_points", []):
            lines.append(f"- {pt}")

        lines.extend(["", "## Key Risks"])
        for rk in draft.get("key_risks", []):
            lines.append(f"- {rk}")

        lines.extend(["", "## Upcoming Catalysts"])
        for cat in draft.get("catalysts", []):
            lines.append(f"- {cat}")

        md_content = "\n".join(lines)
        print("debug:", md_content[:200])

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return md_content
