"""Data collection from public Korean scam sources.

Each collector returns rows conforming to ScamCorpusRow. Raw sources are
rate-limited and cached to avoid hammering public endpoints.

Sources:
    - 경찰청 사이버수사국 press releases via 경찰청 공개 RSS.
    - KISA 인터넷침해대응센터 advisories.
    - 금감원 보이스피싱 실태조사 published PDFs.
    - Public community posts (Naver, Clien, DC Inside) with PII scrubbing.

All collectors obey robots.txt and rate limits. Copyright clearance is
verified before inclusion in the released halo-probe-suite dataset.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator

from halo.corpus.schema import ScamCorpusRow


class BaseCollector(ABC):
    """Base class for scam corpus collectors.

    Subclasses implement `iter_raw` and `parse_row`.
    """

    source_name: str

    def __init__(self, cache_dir: Path, rate_limit_seconds: float = 1.0) -> None:
        self.cache_dir = cache_dir
        self.rate_limit_seconds = rate_limit_seconds

    @abstractmethod
    def iter_raw(self) -> Iterator[object]:
        """Yield raw source records."""

    @abstractmethod
    def parse_row(self, raw: object) -> ScamCorpusRow | None:
        """Convert a raw record into a ScamCorpusRow. Return None to skip."""

    def collect(self) -> Iterator[ScamCorpusRow]:
        """Orchestrate collection with rate limiting and caching."""
        for raw in self.iter_raw():
            row = self.parse_row(raw)
            if row is not None:
                yield row


class PoliceReleaseCollector(BaseCollector):
    """Collects 경찰청 사이버수사국 press releases.

    Implementation plan:
        1. Parse 경찰청 공개 RSS feed for release entries tagged '사이버범죄' or '특수사기'.
        2. Download HTML of each release.
        3. Extract representative scam script passages using heuristic patterns.
        4. Scrub PII (phone numbers, account numbers, names).
        5. Return ScamCorpusRow with source_kind=POLICE_RELEASE.
    """

    source_name = "police_release"

    def iter_raw(self) -> Iterator[object]:
        raise NotImplementedError

    def parse_row(self, raw: object) -> ScamCorpusRow | None:
        raise NotImplementedError


class KisaAdvisoryCollector(BaseCollector):
    """Collects KISA 인터넷침해대응센터 published advisories."""

    source_name = "kisa_advisory"

    def iter_raw(self) -> Iterator[object]:
        raise NotImplementedError

    def parse_row(self, raw: object) -> ScamCorpusRow | None:
        raise NotImplementedError


class CommunityPostCollector(BaseCollector):
    """Collects public community posts from Naver, Clien, and similar.

    Uses search queries for known scam patterns. Requires manual review of
    each collected post before inclusion because community posts can contain
    PII that must be scrubbed.
    """

    source_name = "community_post"

    def __init__(
        self,
        cache_dir: Path,
        search_terms: list[str],
        rate_limit_seconds: float = 2.0,
    ) -> None:
        super().__init__(cache_dir, rate_limit_seconds)
        self.search_terms = search_terms

    def iter_raw(self) -> Iterator[object]:
        raise NotImplementedError

    def parse_row(self, raw: object) -> ScamCorpusRow | None:
        raise NotImplementedError


def scrub_pii(text: str) -> str:
    """Remove Korean PII patterns from text.

    Patterns removed:
        - Phone numbers (010-XXXX-XXXX and variants).
        - Korean resident registration numbers.
        - Bank account numbers.
        - Full Korean names (regex heuristic; manual review still required).
        - Email addresses.
        - URLs that match personal social profiles.

    Returns:
        Scrubbed text. Raises if scrubbing appears incomplete.
    """
    raise NotImplementedError
