"""Korean scam corpus construction and management.

Modules:
    collectors  Source-specific data collection (police, KISA, 금감원, community).
    adversarial SPS-framework-based adversarial perturbation generation.
    schema      Pandera schemas for corpus validation.
"""

from halo.corpus.schema import ScamCorpusRow, ScamCorpusSchema

__all__ = ["ScamCorpusRow", "ScamCorpusSchema"]
