# Raw data

These files are **not stored in git**. Re-create them with:

```powershell
python scripts/download_data.py
```

| File | Source | What it is |
|---|---|---|
| `intel_msom_2022.csv` | Manary, M. P. & Willems, S. P. (2022). *Data Set: 187 Weeks of Customer Forecasts and Orders for Microprocessors from Intel Corporation.* MSOM 24(1):682–689. [doi:10.1287/msom.2020.0933](https://doi.org/10.1287/msom.2020.0933). Public copy from the [INFORMSJoC/2022.0136](https://github.com/INFORMSJoC/2022.0136) repo (Böttcher, Asikis & Fragkos, IJOC, [doi:10.1287/ijoc.2022.0136](https://doi.org/10.1287/ijoc.2022.0136)) | Weekly Intel forecast vs. customer orders by distribution center and SKU, with ASP group |
| `fred_A34SNO.csv` | U.S. Census Bureau M3 via [FRED](https://fred.stlouisfed.org/series/A34SNO) | New orders, Computers & Electronic Products (monthly, $M, seasonally adjusted) |
| `fred_A34SVS.csv` | U.S. Census Bureau M3 via [FRED](https://fred.stlouisfed.org/series/A34SVS) | Shipments, Computers & Electronic Products (monthly, $M, seasonally adjusted) |
| `fred_IPG3344S.csv` | Federal Reserve G.17 via [FRED](https://fred.stlouisfed.org/series/IPG3344S) | Industrial production index, semiconductors & other electronic components |

`DOWNLOAD_LOG.md` records the row counts and file hashes from the last download.

**Columns in the Intel file:** `Distribution Center, Product Offering, Generation, SKU, ASP Group, Week, Forecasted Demand, Customer Orders`
