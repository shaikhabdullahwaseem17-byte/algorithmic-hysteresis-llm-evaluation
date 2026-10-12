# Data Acquisition and Management

This directory contains instructions for retrieving CPI data. Raw data files should not be committed to Git.

## FRED/ALFRED Data Sources

### CPIAUCNS (CPI-U, Not Seasonally Adjusted)

- Series ID: `CPIAUCNS`
- Frequency: Monthly
- Units: Index (2017 = 100)
- Source: U.S. Bureau of Labor Statistics
- FRED API: https://fred.stlouisfed.org/data/CPIAUCNS
- ALFRED API: https://alfred.stlouisfed.org/data/CPIAUCNS

### Retrieval Process

1. **Install FRED API client (optional):**
   ```bash
   pip install fredapi
   ```

2. **Retrieve data programmatically:**
   ```python
   import requests
   
   # FRED API (no key required for basic queries)
   url = "https://api.stlouisfed.org/fred/series/data"
   params = {
       "series_id": "CPIAUCNS",
       "api_key": "[optional key]",
       "file_type": "json"
   }
   response = requests.get(url, params=params)
   ```

3. **ALFRED vintage queries:**
   ```python
   # ALFRED allows querying data as-of a specific date
   # Endpoint: https://alfred.stlouisfed.org/data/CPIAUCNS
   # Include vintage_dates parameter
   ```

### Known Limitations

- CPIAUCNS is not subject to major historical revisions (unlike employment data)
- ALFRED vintage data is available for most historical dates but may have gaps for very old observations
- API rate limits apply; cache retrieved data locally
- No authentication required for basic FRED queries

### Data Schema

Expected columns after retrieval:
- `date`: YYYY-MM-DD (end of month)
- `cpiaucns`: float (index value)
- `bls_release_date`: YYYY-MM-DD (when BLS published this observation)
- `vintage_date`: YYYY-MM-DD (date this record was retrieved/as-of)

### Historical Depth

For the proposed 78-origin sample (2018-01 through 2024-06):
- Minimum required: CPIAUCNS from 2005-01 onwards (to provide 13-month historical context for baseline)
- Target: CPIAUCNS from 1990 onwards (full data availability)

### Data Validation Checks

Before using retrieved data:
1. Verify no missing monthly observations in the relevant period
2. Check for duplicate records (same month, different values)
3. Confirm values are within plausible range (typically 250–330 for 2017=100 index)
4. Verify year-over-year changes are sensible (typically ±5% per month is implausible)
5. Confirm vintage dates are not in the future relative to forecast origins
