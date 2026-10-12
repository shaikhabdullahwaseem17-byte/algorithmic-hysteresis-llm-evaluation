# algorithmic-hysteresis-llm-evaluation

A small, reproducible Phase 2 implementation for a CPI-U nowcasting evaluation pipeline.

## Overview

This repository contains:
- CPIAUCNS data validation utilities
- historical-vintage and cutoff checks
- release-date audit helpers
- year-over-year inflation calculations
- random-walk baseline logic
- evaluation metrics
- configuration and JSONL result logging
- end-to-end mock pipeline tests without real LLM use

## Important Notes

- This project is intentionally designed for synthetic or locally-supplied data in tests.
- No real LLM experiments or external paid APIs are used.
- Real external data access is not assumed and must be validated before claims are made.

## Local Usage

```bash
pip install -r requirements.txt
pytest -q
```

The mock pipeline smoke test exercises the pipeline without running a real model.
