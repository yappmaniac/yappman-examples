# 03 Australia: Aldi shelf prices and Special Buys

Makes two Actor runs. The first searches Aldi Australia for one keyword and sorts the products by unit price. The second fetches Aldi's Special Buys drops dated this week (Monday to Sunday, Sydney time). Coles and Woolworths are not available at the moment. Their rows are read only on runs started by the Actor owner's account (from version 0.1.15), so this example runs Aldi only.

- Actor: [Aldi Australia Price Scraper: Shelf Prices & Special Buys](https://apify.com/yappman/au-supermarket-price-scraper) (`yappman/au-supermarket-price-scraper`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `au_aldi_prices_special_buys.ipynb` in Jupyter Lab and run all cells.

## Actor input

Run 1, search:

```json
{
  "mode": "search",
  "retailers": ["aldi_au"],
  "queries": ["full cream milk"],
  "maxItems": 10
}
```

Run 2, Special Buys. `specialBuysDrops` is the seven dates of the current Sydney week, so the example below shows the shape only.

```json
{
  "mode": "specialBuys",
  "specialBuysDrops": ["YYYY-MM-DD", "YYYY-MM-DD", "YYYY-MM-DD", "YYYY-MM-DD", "YYYY-MM-DD", "YYYY-MM-DD", "YYYY-MM-DD"],
  "maxItems": 60
}
```

The search run passes `max_total_charge_usd=0.03` and the Special Buys run passes `max_total_charge_usd=0.13`. Both have a run timeout of 10 minutes.

## Cost (Free tier)

| Run | Event | Count | Unit price | Most |
|---|---|---|---|---|
| Search | Product row | 10 | $0.002 | $0.02 |
| Search | Actor start | 1 | $0.005 | $0.005 |
| Special Buys | Product row | 60 | $0.002 | $0.12 |
| Special Buys | Actor start | 1 | $0.005 | $0.005 |
| Total | | | | $0.15 |

## How the analysis works

- Search: rows with no `price` are dropped. The unit price (`unitPrice.value` and `unitPrice.measure`) is split into columns, `reduced` is true when `wasPrice` is set and higher than `price`, and the table is sorted by unit price.
- Special Buys: the notebook builds all seven dates (Monday to Sunday) of the current week in Sydney time and sends them as `specialBuysDrops`. Dates Aldi's page does not list are skipped and named in the run's `RUN_SUMMARY` record, which the notebook reads for the Aldi entry.
- Special Buys rows get a `category` from the first element of `categoryPath`, and are counted by `onSaleDate`.

## Output

| File | Contents |
|---|---|
| `output/au_aldi_search.csv` | The Aldi search rows with unit price, reduced flag, name and pack size |
| `output/au_special_buys_this_week.csv` | This week's Special Buys (not written if none are listed) |

## Caveats

- Aldi publishes no barcode, so Aldi rows have an empty `ean` and this example does not match products across shops.
- Coles and Woolworths are not available at the moment. They are read only on runs started by the Actor owner's account. On other accounts those shops are skipped.
- Rows follow the Actor's data terms, not the repository's MIT licence.
