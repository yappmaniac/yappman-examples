# 03 Australia: Coles vs Woolworths, plus Special Buys

Makes two Actor runs. The first searches Coles and Woolworths and compares products one by one on `matchKey`. The second fetches Aldi's Special Buys drops dated this week (Monday to Sunday, Sydney time).

- Actor: [Australia Supermarket Prices](https://apify.com/yappman/au-supermarket-price-scraper) (`yappman/au-supermarket-price-scraper`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `au_coles_woolworths_special_buys.ipynb` in Jupyter Lab and run all cells.

## Actor input

Run 1, search:

```json
{
  "mode": "search",
  "retailers": ["coles", "woolworths"],
  "queries": ["vegemite", "arnotts tim tam", "cadbury dairy milk"],
  "maxItems": 60,
  "excludeMarketplace": true
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

Each run passes `max_total_charge_usd=0.13`.

## Cost (Free tier)

| Run | Event | Count | Unit price | Most |
|---|---|---|---|---|
| Search | Product row | 60 | $0.002 | $0.12 |
| Search | Actor start | 1 | $0.005 | $0.005 |
| Special Buys | Product row | 60 | $0.002 | $0.12 |
| Special Buys | Actor start | 1 | $0.005 | $0.005 |
| Total | | | | $0.25 |

## How the analysis works

- `maxItems` is split evenly between the shops, so up to 30 rows each. Marketplace (third-party) products are excluded.
- Rows with no `price` are dropped. Effective price is the lower of `price` and `loyaltyPrice`. `onSpecial` is true when `wasPrice` is set and higher than `price`.
- Rows are joined on `matchKey`. Where a shop returns several rows with one key, the cheapest is used.
- Only keys present at both Coles and Woolworths are kept. The difference is Coles minus Woolworths, and each product is labelled `coles`, `woolworths` or `same` for the cheaper shop.
- Special Buys: the notebook builds all seven dates (Monday to Sunday) of the current week in Sydney time and sends them as `specialBuysDrops`. Dates Aldi's page does not list are skipped and named in the run's `RUN_SUMMARY` record, which the notebook reads for a count.
- Special Buys rows get a `category` from the first element of `categoryPath`, and are counted by `onSaleDate`.

## Output

| File | Contents |
|---|---|
| `output/au_coles_vs_woolworths.csv` | Products at both shops with prices, difference, cheaper shop, special flags, name and pack size |
| `output/au_special_buys_this_week.csv` | This week's Special Buys (not written if none are listed) |

## Caveats

- Branded products match best because `matchKey` includes the brand.
- Coles rows carry no rating.
- Coles barcodes need `colesProductDetails`, which costs an extra request per product. This example matches on `matchKey` only.
- Rows follow the Actor's data terms, not the repository's MIT licence.
