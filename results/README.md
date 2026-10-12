# Results and Outputs

This directory contains experiment outputs. Do not commit large result files to Git.

## Expected Output Files

### forecast_log.jsonl
- Format: JSON Lines (one JSON object per line)
- Contents: Complete forecast metadata and results for each nowcast
- Columns: forecast_id, experiment_config, forecast_origin, target_month, condition, model_response, parsed_forecast, actual_value, error, revision, etc.
- Purpose: Complete audit trail for reproducibility

### pilot_summary.csv
- Format: CSV
- Contents: Aggregated metrics by condition
- Columns: condition, metric_name, value, unit, count_observations
- Purpose: Quick summary of baseline and model performance

### sample_audit.txt
- Format: Plain text
- Contents: Record of sample verification; exclusions; missing dates; data access limitations
- Purpose: Transparency about which origins were used and why

### condition_b_indicators.csv
- Format: CSV
- Contents: Pre-specified Condition B indicators for all origins (locked before LLM execution)
- Columns: forecast_origin, target_month, fed_action, employment_jobs_added, employment_unemp_rate, ppi_yoy, oil_price_eod, release_dates
- Purpose: Reproducible Condition B specification

## Data Retention Policy

- Raw FRED/ALFRED downloads: Keep local, do not commit
- Forecast logs (JSONL): Commit to version control for reproducibility
- Summary tables (CSV): Commit to version control
- Audit reports (TXT): Commit to version control
- Temporary analysis files: Add to .gitignore

## Results Not Yet Generated

The following do not exist until Phase 3 LLM execution:
- Condition A forecasts (require actual LLM)
- Condition B forecasts (require actual LLM)
- Condition C outputs (require actual LLM)
- Model performance metrics
- Forecast revision analysis
