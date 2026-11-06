"""Download the raw data for the project into data/raw/.

Run:  python scripts/download_data.py

Raw files are NOT committed to git (see .gitignore); this script re-creates them
exactly, so anyone can reproduce the project. That's the "never lose anything" rule
applied to data: we version the *recipe*, not the ingredients.

Sources
-------
1. Intel microprocessor demand (Manary & Willems 2022, MSOM, doi:10.1287/msom.2020.0933).
   Public copy redistributed in the INFORMS Journal on Computing repo for
   Böttcher, Asikis & Fragkos, doi:10.1287/ijoc.2022.0136 (MIT-licensed repo).
2. FRED (Federal Reserve Bank of St. Louis): U.S. Census M3 + Fed industrial production.
"""
from __future__ import annotations

import csv
import hashlib
import io
import sys
import urllib.request
from datetime import date
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

INTEL_URL = ("https://raw.githubusercontent.com/INFORMSJoC/2022.0136/main/"
             "data/MSOM_data/msom.2020.0933.csv")
INTEL_EXPECTED_ROWS = 26_114
INTEL_EXPECTED_COLS = ["Distribution Center", "Product Offering", "Generation", "SKU",
                       "ASP Group", "Week", "Forecasted Demand", "Customer Orders"]

# FRED series: id -> what it measures
FRED_SERIES = {
    "A34SNO": "Manufacturers' New Orders: Computers & Electronic Products (SA, $M, monthly)",
    "A34SVS": "Manufacturers' Value of Shipments: Computers & Electronic Products (SA, $M, monthly)",
    "IPG3344S": "Industrial Production: Semiconductor & Other Electronic Components (SA index, monthly)",
}
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"


def fetch(url: str) -> bytes:
    # Plain default request: FRED stalls on some custom User-Agent strings.
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read()


def download_intel() -> str:
    data = fetch(INTEL_URL)
    rows = list(csv.reader(io.StringIO(data.decode("utf-8-sig"))))
    header, body = rows[0], [r for r in rows[1:] if r]
    assert header == INTEL_EXPECTED_COLS, f"unexpected columns: {header}"
    assert len(body) == INTEL_EXPECTED_ROWS, f"expected {INTEL_EXPECTED_ROWS} rows, got {len(body)}"
    out = RAW / "intel_msom_2022.csv"
    out.write_bytes(data)
    skus = {r[3] for r in body}
    dcs = {r[0] for r in body}
    weeks = {int(r[5]) for r in body}
    return (f"{out.name}: {len(body):,} rows, {len(skus)} SKUs, {len(dcs)} DCs, "
            f"weeks {min(weeks)}-{max(weeks)}, sha256 {hashlib.sha256(data).hexdigest()[:12]}")


def download_fred(sid: str) -> str:
    data = fetch(FRED_URL.format(sid=sid))
    rows = [r for r in csv.reader(io.StringIO(data.decode("utf-8"))) if r]
    assert len(rows) > 12 and rows[0][1] == sid, f"unexpected FRED response for {sid}: {rows[:2]}"
    out = RAW / f"fred_{sid}.csv"
    out.write_bytes(data)
    return f"{out.name}: {len(rows) - 1} months, {rows[1][0]} to {rows[-1][0]}"


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    log, failed = [], False
    jobs = [("Intel MSOM dataset", download_intel)] + [
        (f"FRED {sid}", lambda sid=sid: download_fred(sid)) for sid in FRED_SERIES]
    for name, job in jobs:
        try:
            msg = job()
            print(f"PASS  {name}: {msg}")
            log.append(f"- {msg}")
        except Exception as exc:
            failed = True
            print(f"FAIL  {name}: {type(exc).__name__}: {exc}")
    (RAW / "DOWNLOAD_LOG.md").write_text(
        f"# Raw data download log ({date.today().isoformat()})\n\n" + "\n".join(log) + "\n",
        encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
