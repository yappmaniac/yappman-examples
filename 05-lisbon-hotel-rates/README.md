# 05 Lisbon vendor-rate ladder and the free tracked mode

Makes two Actor runs. The first searches Lisbon for a 2-night stay 30 days out, with each hotel's per-vendor rates, and compares the ladder: who is cheapest and how wide the spread is. The second uses tracked mode to list the hotels the Actor already tracks. An optional third run reads stored history and is off by default.

- Actor: [Google Hotels Prices](https://apify.com/yappman/google-hotels-prices) (`yappman/google-hotels-prices`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `lisbon_hotel_rates.ipynb` in Jupyter Lab and run all cells.

To run the paid history step, set `RUN_HISTORY = True` in the last code cell.

## Actor input

Search. `checkIn` is today plus 30 days and `checkOut` is two days after that, so the dates below show the shape only.

```json
{
  "mode": "search",
  "searches": [
    {"destination": "Lisbon", "checkIn": "YYYY-MM-DD", "checkOut": "YYYY-MM-DD", "adults": 2, "rooms": 1}
  ],
  "includeVendorRates": true,
  "currency": "EUR",
  "maxItems": 15
}
```

Tracked:

```json
{"mode": "tracked"}
```

History (optional, off by default). `hotels` holds at most five hotel ids taken from the tracked list, and the dates are one of its stays.

```json
{
  "mode": "history",
  "hotels": ["<hotelId>"],
  "dates": {"checkIn": "YYYY-MM-DD", "checkOut": "YYYY-MM-DD"}
}
```

The runs pass `max_total_charge_usd` of 0.08 (search), 0.01 (tracked) and 0.06 (history).

## Cost (Free tier)

| Run | Event | Count | Unit price | Most |
|---|---|---|---|---|
| Search | Hotel | 15 | $0.002 | $0.03 |
| Search | Vendor rates | 15 | $0.0025 | $0.0375 |
| Search | Actor start | 1 | $0.005 | $0.005 |
| Tracked | Actor start | 1 | $0.005 | $0.005 |
| History (optional, off) | Hotel with 2+ snapshots | up to 5 | $0.01 | $0.05 |
| History (optional, off) | Actor start | 1 | $0.005 | $0.005 |

Search plus tracked is at most $0.0775. History adds at most $0.055.

## The free tracked mode

Tracked mode charges no Actor events, only the $0.005 start. It lists the hotel ids and stay dates the Actor snapshots (intended weekly). The list is written to the `TRACKED_HOTELS` record of the run's key-value store, not to the dataset. Each tracked city has two stays a week, 14 and 42 days out, for 2 adults and 2 nights.

The notebook filters the tracked list to destinations containing "Lisbon", counts the distinct Lisbon hotels, and marks which searched hotels have history (snapshots are intended weekly).

## How the analysis works

- The ladder has one row per hotel and vendor, cheapest first. Rows with no `perNight` are dropped. Sponsored offers are kept and flagged.
- `rank` is the vendor's position by `perNight` within the hotel (ties share a rank).
- Per hotel, the spread is dearest over cheapest, as a percentage. The notebook also checks whether the lead price (`leadPrice`) equals the cheapest vendor.
- It counts how often each vendor is cheapest. Ties count for every vendor tied.
- It plots the ten widest spreads as a dot-and-line chart.
- History mode returns lead-price snapshots (intended weekly) for tracked hotels. It ignores `maxItems`, so the cost is capped by sending at most five hotels and by `max_total_charge_usd`.

## Output

| File | Contents |
|---|---|
| `output/lisbon_vendor_ladder.csv` | One row per hotel and vendor with rank |

The spread table, tracked list and chart are shown inline only.

## Caveats

- Prices are Google's pre-tax figures in the chosen currency (EUR here).
- History costs $0.01 per hotel with two or more snapshots. One-snapshot rows are free. History is in USD for 2 adults.
- Rows follow the Actor's data terms, not the repository's MIT licence.
