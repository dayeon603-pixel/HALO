"""Tests for halo.corpus.schema."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from halo.corpus.schema import ScamCategory, ScamCorpusRow, SourceKind


def _sample_row(**overrides: object) -> ScamCorpusRow:
    defaults: dict[str, object] = dict(
        row_id="test-0001",
        text="서울중앙지방검찰청 김검사입니다. 귀하의 계좌 확인이 필요합니다.",
        category=ScamCategory.VOICE_PHISHING,
        key_signals=["수사기관 사칭", "즉시 연락 요구", "계좌 확인 유도"],
        source_kind=SourceKind.POLICE_RELEASE,
        collected_at=datetime(2026, 4, 18, tzinfo=timezone.utc),
        annotator_initials="DK",
    )
    defaults.update(overrides)
    return ScamCorpusRow(**defaults)


def test_valid_row_constructs() -> None:
    row = _sample_row()
    assert row.category is ScamCategory.VOICE_PHISHING
    assert row.source_kind is SourceKind.POLICE_RELEASE


def test_empty_text_rejected() -> None:
    with pytest.raises(ValidationError):
        _sample_row(text="")


def test_too_many_key_signals_rejected() -> None:
    with pytest.raises(ValidationError):
        _sample_row(key_signals=["a", "b", "c", "d", "e", "f"])


def test_annotator_initials_max_length() -> None:
    with pytest.raises(ValidationError):
        _sample_row(annotator_initials="DAYEON")


def test_adversarial_row_has_parent_and_perturbation() -> None:
    row = _sample_row(
        row_id="adv-0001",
        source_kind=SourceKind.ADVERSARIAL,
        parent_row_id="test-0001",
        perturbation="emoji_space_inject",
    )
    assert row.parent_row_id == "test-0001"
    assert row.perturbation == "emoji_space_inject"
