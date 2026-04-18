"""SPS-framework-based adversarial perturbations for the Korean scam corpus.

Given an original text, generate structured variations that preserve meaning
but evade keyword-based detection. Target approximately 20 percent of the
corpus as adversarial samples to train robust recognition.

Perturbation strategies:
    1. Emoji or whitespace insertion.
    2. Character substitution (case, hanja, similar-looking Roman).
    3. Similar domain substitution in URLs.
    4. Context reordering while preserving meaning.

Reference:
    See Structured Perturbation Stability (SPS) Framework, team repo.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Callable


Perturbation = Callable[[str], str]


@dataclass(frozen=True, slots=True)
class PerturbationResult:
    original_text: str
    perturbed_text: str
    method: str


def emoji_space_inject(text: str, rate: float = 0.2) -> str:
    """Inject emojis or spaces into selected character boundaries.

    Example:
        서울중앙지검 -> 서울중앙지✨검✨
    """
    raise NotImplementedError


def char_substitute(text: str) -> str:
    """Substitute characters with case or script variants.

    Example:
        LG화학 -> Lg화학, LG化学
    """
    raise NotImplementedError


def similar_domain(text: str) -> str:
    """Replace legitimate-looking domains with phishing variants.

    Example:
        www.gov.kr -> gov24-bonus.kr
    """
    raise NotImplementedError


def context_reorder(text: str) -> str:
    """Reorder sentences while preserving meaning via Korean clause analysis.

    Uses a light-weight clause splitter. Does not reorder across negation
    boundaries.
    """
    raise NotImplementedError


PERTURBATIONS: dict[str, Perturbation] = {
    "emoji_space_inject": emoji_space_inject,
    "char_substitute": char_substitute,
    "similar_domain": similar_domain,
    "context_reorder": context_reorder,
}


def perturb(text: str, method: str, seed: int = 42) -> PerturbationResult:
    """Apply a named perturbation to text.

    Args:
        text: Original Korean text.
        method: Name of the perturbation in PERTURBATIONS.
        seed: Random seed for reproducibility.

    Returns:
        PerturbationResult with original, perturbed, and method name.

    Raises:
        KeyError if method is unknown.
    """
    if method not in PERTURBATIONS:
        msg = f"Unknown perturbation: {method}"
        raise KeyError(msg)
    random.seed(seed)
    perturbed = PERTURBATIONS[method](text)
    return PerturbationResult(
        original_text=text, perturbed_text=perturbed, method=method
    )


def generate_adversarial_set(
    originals: list[str], target_ratio: float = 0.2, seed: int = 42
) -> list[PerturbationResult]:
    """Generate adversarial perturbations for a fraction of the corpus.

    Args:
        originals: Source Korean texts.
        target_ratio: Fraction of corpus to perturb.
        seed: Random seed.

    Returns:
        List of PerturbationResult. Length is approximately len(originals) * target_ratio.
    """
    raise NotImplementedError
