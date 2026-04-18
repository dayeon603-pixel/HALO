"""Automatic generation of 경찰청 사이버수사대 신고 양식.

Takes a classified scam event and produces a filled report form (PDF or HWP)
ready for submission to 사이버범죄 신고 system.

Workflow:
    1. Read the HALO audit log entries for the incident.
    2. Summarize evidence using Solar-pro API with a structured prompt.
    3. Render the form template with summarized fields.
    4. Return path to generated PDF and a ready-to-send HWP copy.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True, slots=True)
class IncidentSummary:
    """Pre-formatted incident data for the report form."""

    incident_id: str
    occurred_at: datetime
    category: str
    summary_kr: str
    evidence_points: list[str]
    financial_loss_krw: int | None = None


def generate_report(summary: IncidentSummary, template_path: Path, out_dir: Path) -> Path:
    """Generate filled report PDF from template.

    Args:
        summary: Structured incident data.
        template_path: Path to the blank form template.
        out_dir: Output directory for the generated PDF.

    Returns:
        Path to generated PDF.
    """
    raise NotImplementedError


def summarize_with_solar_pro(audit_log_entries: list[dict], api_key: str) -> IncidentSummary:
    """Call Upstage Solar-pro to produce a human-readable incident summary.

    Args:
        audit_log_entries: HALO event records for the incident.
        api_key: Upstage API credential.

    Returns:
        IncidentSummary suitable for generate_report.
    """
    raise NotImplementedError
