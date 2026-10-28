# 09 Lisbon hotel price history

Reads the lead-price snapshots the Actor has stored for Lisbon hotels and plots price per night against the date each was read. Two runs: tracked mode to find a stay with stored snapshots, then history mode for up to five hotels.

- Actor: [Hotel Prices from Google Hotels: Vendor Rates, History](https://apify.com/yappman/google-hotels-prices) (`yappman/google-hotels-prices`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `hotel_price_history.ipynb` in Jupyter Lab and run all cells.

## Actor input

Tracked. The list is written to the `TRACKED_HOTELS` record of the run's key-value store.

```json
{"mode": "tracked"}
```

History. `hotels` holds at most five hotel ids taken from that list, and the dates are one of its stays (2 adults, 1 room).

```json
{
  "mode": "history",
  "hotels": ["<hotelId>"],
  "dates": {"checkIn": "YYYY-MM-DD", "checkOut": "YYYY-MM-DD"}
}
```

The runs pass `max_total_charge_usd` of 0.01 (tracked) and 0.06 (history), and a 10-minute run timeout.

## Cost (Free tier)

| Run | Event | Count | Unit price | Most |
|---|---|---|---|---|
| Tracked | Actor start | 1 | $0.005 | $0.005 |
| History | Rate history | up to 5 | $0.01 | $0.05 |
| History | Actor start | 1 | $0.005 | $0.005 |

At most $0.06. A hotel with only one stored snapshot is not charged for history.

## Output

The history rows are written to `output/lisbon_price_history.csv` (git-ignored) and plotted. Rows belong to the Actor's data terms, not to this repository's MIT licence.
