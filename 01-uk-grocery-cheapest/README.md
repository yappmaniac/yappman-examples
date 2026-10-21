# 01 UK grocery: cheapest effective price

Runs one search across Tesco, Sainsbury's, Asda, Aldi and Morrisons. Groups the rows into products by barcode (EAN), with `matchKey` as the fallback. Reports the cheapest effective price for each product and the saving against the dearest retailer.

- Actor: [UK Grocery Prices](https://apify.com/yappman/uk-supermarket-price-scraper) (`yappman/uk-supermarket-price-scraper`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `uk_grocery_cheapest.ipynb` in Jupyter Lab and run all cells.

## Actor input

```json
{
  "mode": "search",
  "retailers": ["tesco", "sainsburys", "asda", "aldi", "morrisons"],
  "queries": ["heinz baked beans", "pg tips tea bags", "lurpak spreadable"],
  "maxItems": 100
}
```

`maxItems` is split equally between the shops, so up to 20 rows each. The run also passes `max_total_charge_usd=0.26`.

## Cost (Free tier)

| Event | Count | Unit price | Most |
|---|---|---|---|
| Product row | 100 | $0.0025 | $0.25 |
| Actor start | 1 | $0.005 | $0.005 |
| Total | | | $0.255 |

## How the analysis works

- Effective price is the lower of `price` and `loyaltyPrice`. Rows with no `price` are dropped. Multi-buy offers in `promotionText` are not modelled.
- A barcode is usable when it has 8 to 14 digits, a valid GS1 check digit, at least 8 significant digits (so zero-padded internal IDs are dropped), and is not an in-store code (prefix 2 or 02).
- Rows sharing a usable barcode are the same product (union-find).
- A row with no usable barcode joins a barcode group only when exactly one group carries the same `matchKey`. If no barcode group has that key, it groups with other barcode-less rows on `matchKey`.
- Rows whose barcodes differ are never merged by `matchKey`.
- Per product, the cheapest row is chosen among rows not reported out of stock (`inStock` of false). If every row is out of stock, all rows are considered.
- `matchedBy` records `ean`, `matchKey` or `ean+matchKey`.
- Only products found at two or more retailers are kept in the matched table, sorted by saving.

## Output

| File | Contents |
|---|---|
| `output/uk_cheapest_by_retailer.csv` | Effective price for each matched product at each retailer |

## Caveats

- Branded products give the best barcode matches. Own-label lines differ between retailers.
- `matchKey` is a normalised name and pack size. Its format changes no earlier than 4 November 2026. Do not compare keys saved before and after that date.
- Prices are as each retailer's service shows them at run time: no store is chosen for Tesco and Sainsbury's; one fixed store or service point is used for Asda and Aldi.
- Rows and prices follow the Actor's data terms, not the repository's MIT licence.
