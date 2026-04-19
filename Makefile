# HALO common commands.

.PHONY: help install dev lint format test typecheck build-corpus train evaluate demo clean

help:
	@echo "HALO development targets"
	@echo ""
	@echo "  install         Install runtime dependencies"
	@echo "  dev             Install dev dependencies and pre-commit hooks"
	@echo "  lint            Run ruff and black check"
	@echo "  format          Run ruff fix and black format"
	@echo "  test            Run pytest"
	@echo "  typecheck       Run mypy"
	@echo "  build-corpus    Build Korean scam corpus v0"
	@echo "  train           Fine-tune Mi:dm 2.0 Mini with LoRA"
	@echo "  evaluate        Evaluate classifier on test set"
	@echo "  demo            Run Solar-pro classifier demo"
	@echo "  clean           Remove build artifacts"

install:
	pip install -e .

dev:
	pip install -e ".[dev,docs]"
	pre-commit install

lint:
	ruff check src tests
	black --check src tests

format:
	ruff check --fix src tests
	black src tests

test:
	pytest tests -v --tb=short

typecheck:
	mypy src

build-corpus:
	python -m halo.scripts.build_corpus \
		--sources police,kisa,community \
		--output data/processed/corpus_v0.parquet

train:
	python -m halo.training.lora_finetune \
		--config configs/model_midm_mini.yaml

evaluate:
	python -m halo.training.evaluate \
		--config configs/eval.yaml

demo:
	python -m halo.demo.classifier_demo

clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
