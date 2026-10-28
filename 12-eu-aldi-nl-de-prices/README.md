# 12 Netherlands and Germany: Aldi shelf prices in EUR

Makes one Actor run that reads two category pages: fresh dairy at Aldi Netherlands (`aldi.nl`) and milk at Aldi Nord Germany (`aldi-nord.de`). For each shop it sorts the products by the shop's own unit price, within each measure, and counts the products that show none.

- Actor: [Aldi Netherlands & Germany Price Scraper: Shelf Prices (EUR)](https://apify.com/yappman/nl-de-supermarket-price-scraper) (`yappman/nl-de-supermarket-price-scraper`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `eu_aldi_nl_de_prices.ipynb` in Jupyter Lab and run all cells.

## Actor input

```json
{
  "mode": "category",
  "categoryUrls": [
    "https://www.aldi.nl/producten/zuivel-eieren-boter/verse-zuivel.html",
    "https://www.aldi-nord.de/sortiment/milchprodukte/milch-milchgetraenke.html"
  ],
  "maxItems": 30
}
```

Category mode takes the shop from each page address, so the input has no `retailers` list. `maxItems` is shared evenly between the two shops, so each returns at most 15 rows. The run passes `max_total_charge_usd=0.055` and has a run timeout of 10 minutes.

## Cost (Free tier)

| Run | Event | Count | Unit price | Most |
|---|---|---|---|---|
| Category | Product row | 30 | $0.0015 | $0.045 |
| Category | Actor start | 1 | $0.005 | $0.005 |
| Total | | | | $0.05 |

## How the analysis works

- The notebook reads the run's `RUN_SUMMARY` record and prints, per shop, its status, the rows returned and the records skipped for having no current price.
- The unit price (`unitPrice.value` and `unitPrice.measure`) is split into columns. `reduced` is true when `wasPrice` is set and higher than `price`. `category` is the last element of `categoryPath`.
- Each shop's rows are sorted by unit price within each measure (kg, l and so on), because a price per kg and a price per litre are not comparable. Products that show no unit price come last.

## Output

| File | Contents |
|---|---|
| `output/eu_aldi_nl_prices.csv` | The aldi.nl rows with unit price, reduced flag and category |
| `output/eu_aldi_nord_de_prices.csv` | The aldi-nord.de rows, with the same columns |

## Caveats

- Unit prices are the shops' own. Where a shop shows none, `unitPrice` is empty: the Actor never calculates one.
- The two shops sell different ranges and name products in Dutch and German, so this example does not compare products across shops.
- Aldi shows no barcode, so `ean` is always empty.
- At aldi-nord.de the bottle deposit (Pfand) is not a field.
- Rows follow the Actor's data terms, not the repository's MIT licence.
