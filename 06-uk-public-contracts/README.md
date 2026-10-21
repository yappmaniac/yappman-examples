# 06 UK public contracts: the newest notices

Makes one Actor run: a search of Find a Tender and Contracts Finder, newest first, capped at 20 notices. Each row is one government procurement notice in one fixed schema, designed not to include individuals' details. The notebook shows the rows as a table, then reads the run summary to see whether either service left days uncovered.

- Actor: [UK Public Contracts Lookup](https://apify.com/yappman/contracts-lookup) (`yappman/contracts-lookup`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `uk_public_contracts.ipynb` in Jupyter Lab and run all cells.

## Actor input

```json
{
  "mode": "search",
  "sources": ["fts", "cf"],
  "maxItems": 20
}
```

The run passes `max_total_charge_usd=0.11` and a run timeout of 10 minutes. Public Contracts Scotland is opt-in and is not read here.

## Cost (Free tier)

| Event | Count | Unit price | Most |
|---|---|---|---|
| Notice | 20 | $0.005 | $0.10 |
| Run | 1 | $0.005 | $0.005 |
| Total | | | $0.105 |

The price is the same on every plan.

## How the analysis works

- Rows come out newest `publishedAt` first. A missing value is `null`.
- The notebook shows `publishedAt`, `source`, `title`, `buyer`, `value`, `currency`, `stage`, `deadline` and `regions`. The list of regions is joined into one string.
- It then reads the `RUN_SUMMARY` record and prints `status`, `pushed`, `readData` and `runCharged`, and for each source `noticesRead`, `missingDays` and `staleSince`.
- Find a Tender is currently read from its API only, so a wide search can come back partial. The summary names the days that were missing.
- A procurement published on both services is two rows. `reconcileKey` probably matches them, so join on it yourself.

## Output

Nothing is written to disk. The table and the summary are shown in the notebook only.

## Caveats

- Contains public sector information licensed under the Open Government Licence v3.0. Keep this attribution with any data you republish.
- Rows hold no contact names, emails, phone numbers, addresses or supplier names. Titles are redacted by pattern, so a name written some other way in a title is not caught.
- Rows follow the Actor's data terms, not the repository's MIT licence.
