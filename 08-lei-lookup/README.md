# 08 LEI lookup: one Legal Entity Identifier

Makes one Actor run in LEI mode with a single LEI. Each row is one entity from the daily Golden Copy of the Global LEI Index, in one fixed schema designed not to include individuals' details. The notebook shows the row as a table, then reads the run summary, which lists anything refused or not found.

- Actor: [LEI Lookup](https://apify.com/yappman/lei-lookup) (`yappman/lei-lookup`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `lei_lookup.ipynb` in Jupyter Lab and run all cells.

## Actor input

```json
{
  "mode": "lei",
  "leis": ["2138002P5RNKC5W2JZ46"]
}
```

The run passes `max_total_charge_usd=0.005` and a run timeout of 10 minutes.

## Cost (Free tier)

| Event | Count | Unit price | Most |
|---|---|---|---|
| Entity returned | 1 | $0.004 | $0.004 |
| Total | | | $0.004 |

There is no start fee. An LEI that is invalid or not found costs nothing. In LEI mode the list of LEIs (1 to 1,000) is the cap, because `maxItems` applies only to name and status searches.

## How the analysis works

- Each LEI is checked as ISO 17442 before any request. A malformed one is refused on its own and costs nothing.
- Rows come back in input order.
- The notebook shows `lei`, `legalName`, `registrationStatus`, `entityStatus`, `jurisdiction`, `legalForm`, `legalAddress`, `nextRenewalDate`, `withheld` and `goldenCopyDate`.
- `legalAddress` is shown as city, region, country.
- It then reads the `RUN_SUMMARY` record and prints `status`, `mode`, `pushed`, `found`, `requested`, `notFound`, `refused`, `unavailable`, `withheldPersons` and `goldenCopyDate`.

## Output

Nothing is written to disk. The table and the summary are shown in the notebook only.

## Caveats

- Where the entity is a person, such as a sole proprietor, the name, register number and addresses are `null` and listed in `withheld`. The LEI, statuses and dates are still returned.
- Addresses are country, region and city only. No street, number or postcode is read.
- The data is the Global LEI Index published by GLEIF, under CC0. No attribution is required. This is not affiliated with, or endorsed by, GLEIF or any LEI issuer.
- Rows follow the Actor's data terms, not the repository's MIT licence.
