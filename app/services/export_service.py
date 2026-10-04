import os
from typing import Optional
from app.integrations.s3_client import S3Service


class ExportService:
    """Service to export research reports into readable formats and cloud storage."""

    def __init__(self):
        self.s3_service = S3Service()

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

        approved = report_data.get("approved")
        feedback = report_data.get("feedback")
        if approved is not None:
            lines.extend([
                "",
                "## Senior Analyst Certification (HITL)",
                f"- **Status:** {'APPROVED' if approved else 'REVISION REQUESTED'}",
                f"- **Analyst Feedback:** {feedback if feedback else 'None'}",
            ])

        md_content = "\n".join(lines)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return md_content

    def export_to_s3(self, report_data: dict, key: Optional[str] = None) -> Optional[str]:
        """Generate markdown memo and upload directly to AWS S3 bucket."""
        ticker = report_data.get("ticker", "STOCK").upper()
        if not key:
            key = f"reports/{ticker}_investment_memorandum.md"

        dummy_path = f"/tmp/{ticker}_report.md"
        content = self.to_markdown(report_data, dummy_path)

        success = self.s3_service.upload_bytes(
            content.encode("utf-8"),
            key=key,
            content_type="text/markdown",
        )
        if success:
            return f"s3://{self.s3_service.bucket}/{key}"
        return None
