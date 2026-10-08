# 02 UK daily basket: 30-day price history

Reads the free daily basket dataset `ynAT9NPps2EdjMOJa`, published by the UK Grocery Prices Actor. It holds the same 212 staple products from four retailers, priced every day. The notebook builds a per-product price history for the last 30 days and a simple chained index for each retailer.

- Actor: [UK Grocery Prices](https://apify.com/yappman/uk-supermarket-price-scraper) (publishes the dataset; this notebook does not run it)
- Data: https://data.yappman.com
- Free sample: [Kaggle, CC BY 4.0](https://www.kaggle.com/datasets/russellyapp/uk-supermarket-prices-daily-212-item-basket)

## How to run

1. Set up the environment as described in the root README.
2. Open `uk_basket_price_history.ipynb` in Jupyter Lab and run all cells.

`APIFY_TOKEN` is optional here because the dataset is public. If it is set, the notebook uses it.

## Input

No Actor is run, so there is no Actor input. The notebook reads dataset `ynAT9NPps2EdjMOJa` with `iterate_items(fields=..., desc=True)` for these fields: `retailer`, `retailerProductId`, `name`, `packSize`, `price`, `loyaltyPrice`, `inStock`, `scrapedAt`.

## Cost (Free tier)

| Event | Count | Unit price | Most |
|---|---|---|---|
| Actor events | 0 | n/a | $0.00 |

Reading a dataset starts no Actor and charges no events. There is no `maxItems`. The cap is the history window: reading stops at the first row older than the cutoff.

## History available

History began on 24 September 2026, so fewer than 30 days exist until late October 2026. The notebook uses what exists and prints how many days it found.

## How the analysis works

- Reads newest first (`desc=True`). The cutoff is today (UTC, midnight) minus 29 days. Reading stops at the first row older than the cutoff.
- Each product is keyed as `retailer:retailerProductId`. Where a product has several rows on one day, the latest is kept. Rows with no `price` are dropped.
- Effective price is the lower of `price` and `loyaltyPrice`.
- Per product it reports first, latest, low and high price, the number of price changes, and percentage change from first to latest.
- The index is a chained Jevons index per retailer. Each day moves by the geometric mean of price relatives for products priced on both that day and the day before. The first day is 100.
- The index is a quick illustration, not the published [Shelf-Price Index](https://data.yappman.com/shelf-price-index).

## Output

| File | Contents |
|---|---|
| `output/basket_history_wide.csv` | Effective price by date (rows) and product (columns) |
| `output/basket_history_summary.csv` | Per-product first, latest, low, high, price changes, change % |

The notebook also draws an index chart inline. It is not saved.

## Caveats

- Basket rows are the Actor publisher's data, not covered by the MIT licence.
- Nothing collected is committed. `output/` is git-ignored.
