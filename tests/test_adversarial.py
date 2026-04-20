"""Tests for adversarial perturbation interface."""

import pytest

from halo.corpus.adversarial import (
    PERTURBATIONS,
    PerturbationResult,
    char_substitute,
    context_reorder,
    emoji_space_inject,
    generate_adversarial_set,
    perturb,
    similar_domain,
)


def test_perturbations_registry_contains_expected_methods() -> None:
    expected = {
        "emoji_space_inject",
        "char_substitute",
        "similar_domain",
        "context_reorder",
    }
    assert set(PERTURBATIONS.keys()) == expected


def test_perturb_unknown_method_raises() -> None:
    with pytest.raises(KeyError, match="Unknown perturbation"):
        perturb("some text", method="nonexistent")


def test_perturbation_result_fields() -> None:
    result = PerturbationResult(
        original_text="원문",
        perturbed_text="변형",
        method="emoji_space_inject",
    )
    assert result.original_text == "원문"
    assert result.perturbed_text == "변형"
    assert result.method == "emoji_space_inject"


@pytest.mark.parametrize("method_name", list(PERTURBATIONS.keys()))
def test_each_method_is_callable(method_name: str) -> None:
    method = PERTURBATIONS[method_name]
    assert callable(method), f"{method_name} is not callable"


@pytest.mark.parametrize(
    "fn",
    [emoji_space_inject, char_substitute, similar_domain, context_reorder],
)
def test_unimplemented_raises_not_implemented(fn: object) -> None:
    assert callable(fn)
    with pytest.raises(NotImplementedError):
        fn("테스트 텍스트")  # type: ignore[operator]


def test_generate_adversarial_set_unimplemented() -> None:
    with pytest.raises(NotImplementedError):
        generate_adversarial_set(["샘플1", "샘플2"], target_ratio=0.2, seed=42)
