"""Pandera schema for the Korean scam corpus.

Every row has a stable identifier, the text content, category label, key
signals, source attribution, and metadata. Adversarial perturbations carry
a pointer to the original row.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

import pandera as pa
from pandera.typing import Series
from pydantic import BaseModel, Field


class ScamCategory(str, Enum):
    VOICE_PHISHING = "voice_phishing"
    ROMANCE_SCAM = "romance_scam"
    INVESTMENT_SCAM = "investment_scam"
    LOAN_SCAM = "loan_scam"
    SUBSIDY_SCAM = "subsidy_scam"
    FAMILY_IMPERSONATION = "family_impersonation"
    BENIGN = "benign"


class SourceKind(str, Enum):
    POLICE_RELEASE = "police_release"
    KISA_ADVISORY = "kisa_advisory"
    FSS_REPORT = "fss_report"
    COMMUNITY_POST = "community_post"
    SYNTHETIC = "synthetic"
    ADVERSARIAL = "adversarial"


class ScamCorpusRow(BaseModel):
    """Single corpus row.

    Attributes:
        row_id: Stable UUIDv7 identifier. Sortable by time.
        text: Raw Korean text of the message after PII scrubbing.
        category: Scam taxonomy label or benign.
        key_signals: 3 to 5 phrases that justify the label.
        source_kind: Origin of the sample.
        source_ref: Source URL or internal reference.
        collected_at: UTC timestamp of collection.
        parent_row_id: For adversarial samples, the row_id of the original.
        perturbation: The SPS perturbation name if this row is adversarial.
        is_holdout: Whether this row is reserved for held-out evaluation.
        annotator_initials: Labeler identifier for audit.
        secondary_reviewer_initials: Second-reviewer if applicable.
    """

    row_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1, max_length=4096)
    category: ScamCategory
    key_signals: list[str] = Field(default_factory=list, max_length=5)
    source_kind: SourceKind
    source_ref: str | None = None
    collected_at: datetime
    parent_row_id: str | None = None
    perturbation: str | None = None
    is_holdout: bool = False
    annotator_initials: str = Field(..., min_length=1, max_length=4)
    secondary_reviewer_initials: str | None = None


ScamCorpusSchema = pa.DataFrameSchema(
    {
        "row_id": pa.Column(str, unique=True),
        "text": pa.Column(str, checks=pa.Check.str_length(min_value=1, max_value=4096)),
        "category": pa.Column(str, checks=pa.Check.isin([c.value for c in ScamCategory])),
        "key_signals": pa.Column(object),
        "source_kind": pa.Column(str, checks=pa.Check.isin([s.value for s in SourceKind])),
        "source_ref": pa.Column(str, nullable=True),
        "collected_at": pa.Column("datetime64[ns]"),
        "parent_row_id": pa.Column(str, nullable=True),
        "perturbation": pa.Column(str, nullable=True),
        "is_holdout": pa.Column(bool),
        "annotator_initials": pa.Column(str, checks=pa.Check.str_length(min_value=1, max_value=4)),
        "secondary_reviewer_initials": pa.Column(str, nullable=True),
    },
    strict=True,
    coerce=True,
)


def validate(frame_like: object) -> object:
    """Validate a DataFrame-like object against ScamCorpusSchema.

    Raises:
        pandera.errors.SchemaError on violation.
    """
    return ScamCorpusSchema.validate(frame_like)
