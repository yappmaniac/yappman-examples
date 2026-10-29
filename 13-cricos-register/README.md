# 13 Australian education providers (CRICOS)

Two runs: a search of the CRICOS register for providers in New South Wales (10 rows), then a lookup of two of those providers by provider code.

- Actor: [CRICOS Register Lookup (Australia)](https://apify.com/yappman/cricos-register) (`yappman/cricos-register`)
- Data: https://data.yappman.com

Contains data from the Commonwealth Register of Institutions and Courses for Overseas Students (CRICOS), Department of Education, Australian Government, licensed under Creative Commons Attribution 2.5 Australia (CC BY 2.5 AU). This Actor filters and reshapes the data; changes were made.

Not affiliated with or endorsed by the Department of Education.

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `cricos_register.ipynb` in Jupyter Lab and run all cells.

## Actor input

Search.

```json
{"mode": "search", "states": ["NSW"], "maxItems": 10}
```

Lookup. `providerCodes` holds 1 to 20 codes; the notebook uses the first two from the search.

```json
{"mode": "lookup", "providerCodes": ["<providerCode>", "<providerCode>"]}
```

Both runs pass `max_total_charge_usd=0.03` and have a run timeout of 10 minutes.

## Cost (Free tier)

| Run | Event | Count | Unit price | Most |
|---|---|---|---|---|
| Search | Record | 10 | $0.002 | $0.02 |
| Lookup | Record | 2 | $0.002 | $0.004 |
| Total | | | | $0.024 |

There is no start fee. A refused run or one that returns nothing is not charged.

## Output

The search rows are written to `output/cricos_search.csv` (git-ignored). A provider's name is left out when the Actor cannot tell an organisation from a person; those rows carry `nameWithheld: true`. The notebook shows provider codes and the register's own fields. Rows belong to the Actor's data terms, not to this repository's MIT licence.
