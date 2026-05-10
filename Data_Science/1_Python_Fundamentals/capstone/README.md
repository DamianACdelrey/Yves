### Capstone — Module 1: Transaction Summary

A small, self-contained Python artifact that takes a messy CSV of crypto trades, cleans it, builds a structured summary, and writes a single readable report.

#### Purpose

Practice the end-to-end pipeline `read ➜ clean ➜ summarize ➜ save` using only the Python standard library, so each step is explicit and easy to reason about.

#### Files

| File | Role |
| --- | --- |
| `transactions.csv` | Input: raw trades with realistic noise (whitespace, mixed case, one duplicate, one row with missing numeric fields). |
| `transaction_summary.ipynb` | The artifact. One numbered section per pipeline step, with a short narrative before each block of code. |
| `summary.txt` | Output: human-readable report regenerated every time the notebook is run from top to bottom. |

#### Input

`transactions.csv` columns:

`ID, Type, Subtype, Datetime, Amount, Amount currency, Value, Value currency, Rate, Rate currency`

Each row is one market trade. The raw file intentionally contains:

- extra whitespace inside cells (`'475166337 '`, `' Buy '`)
- inconsistent casing (`'sell'`, `'SELL'`, `'btc'`, `'eur'`, `'market'`)
- one duplicate row (same `ID` repeated)
- one row with empty numeric fields

#### Processing steps

1. **Read** — `csv.DictReader` returns one dictionary per row using the header line as keys.
2. **Clean** — strip whitespace, drop duplicate `ID`s, drop rows with empty numeric fields, normalize text to title case, currencies to upper case, cast `Amount` / `Value` / `Rate` to `float`, and parse `Datetime` into a `datetime` object.
3. **Summarize** — group by `Subtype` (Buy / Sell) and compute count, total amount in BTC, total value in EUR, and average price (EUR per BTC). Also report the date range and the net BTC position (`buys - sells`).
4. **Save** — format the summary dict as plain text and write it to `summary.txt`.

#### Final result

Running the notebook on the included `transactions.csv` drops 2 rows (1 duplicate, 1 with missing values) and produces `summary.txt`:

```
Transactions summary
==============================

Total transactions: 9
Date range: 2025-11-02 to 2025-11-10
Net BTC position: 0.03625000 BTC

By subtype
------------------------------
Buy:
  count:        4
  total amount: 0.15000000 BTC
  total value:  9462.65 EUR
  avg price:    63084.33 EUR/BTC
Sell:
  count:        5
  total amount: 0.11375000 BTC
  total value:  7313.00 EUR
  avg price:    64290.11 EUR/BTC
```

#### How to run

From this folder, open `transaction_summary.ipynb` in VS Code / Cursor / Jupyter and run all cells from top to bottom. The notebook is idempotent: same input → same `summary.txt`.
