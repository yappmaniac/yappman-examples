# yappman examples

Worked examples, written as Python notebooks, for yappman's Apify Actors. Each notebook runs an Actor (or reads a public dataset), analyses the result with pandas, and writes its output to a local `output/` folder. Every paid run has a hard spend cap.

## Examples

| Folder | What it does | Actor(s) | Most it costs per run (Free tier) |
|---|---|---|---|
| [01-uk-grocery-cheapest](01-uk-grocery-cheapest) | Finds the cheapest effective price for each product across Tesco, Sainsbury's, Asda, Aldi and Morrisons | UK Grocery Prices | $0.255 |
| [02-uk-basket-price-history](02-uk-basket-price-history) | Builds a 30-day price history and a chained index from the free daily basket dataset | None (public dataset) | $0.00 |
| [03-au-coles-woolworths-special-buys](03-au-coles-woolworths-special-buys) | Compares Coles and Woolworths on `matchKey` and lists this week's Aldi Special Buys | Australia Supermarket Prices | $0.25 |
| [04-leeds-property-planning-map](04-leeds-property-planning-map) | Maps Leeds listings coloured by planning constraints and nearby applications | UK Property Listings + Planning | $0.365 |
| [05-lisbon-hotel-rates](05-lisbon-hotel-rates) | Compares vendor rates for Lisbon hotels and reads the hotels the Actor tracks, using the free tracked mode | Google Hotels Prices | $0.0775 (plus $0.055 optional history, off by default) |

All five together cost about $0.95 at most. Apify's Free plan includes monthly platform credit that covers this.

## Actors and data

| Actor | Store page |
|---|---|
| UK Grocery Prices | https://apify.com/yappman/uk-supermarket-price-scraper |
| Australia Supermarket Prices | https://apify.com/yappman/au-supermarket-price-scraper |
| UK Property Listings + Planning | https://apify.com/yappman/uk-property-listings |
| Google Hotels Prices | https://apify.com/yappman/google-hotels-prices |

Bulk history and weekly catalogues: https://data.yappman.com. The Shelf-Price Index: https://data.yappman.com/shelf-price-index.

## Setup

You need Python 3.11 or later and an Apify API token. Create a token at https://console.apify.com/settings/integrations.

Example 02 works without a token because its dataset is public.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export APIFY_TOKEN="your-token-here"
jupyter lab
```

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:APIFY_TOKEN = "your-token-here"
jupyter lab
```

`.env.example` shows the variable name. Notebooks read `APIFY_TOKEN` from the environment, not from a `.env` file, so export it in your shell before starting `jupyter lab`. Never commit a real token.

## How spend is capped

Every paid run does two things:

- Sets `maxItems` in the Actor input.
- Passes `max_total_charge_usd` to apify-client's `call()`.

The Actors use pay-per-event pricing, so they charge only their own events (for example a start fee and a price per row). Platform compute is not billed on top.

Prices quoted in these READMEs are Free-tier event prices as of October 2026. Paid Apify plans pay less per event. Check each Store page for current prices.

`apify-client` is pinned to 3.2.1 on purpose. The code uses the 3.x API, where `call()` returns a Run object with attributes such as `default_dataset_id`.

## What is not in this repo

- No tokens.
- No collected data.
- No retailer or portal logos.

Notebooks are committed without outputs. Everything a notebook collects is written to `output/`, which git ignores. Run `python scripts/check_repo.py` before committing. CI runs it too.

## Upcoming Actor changes

- The UK Actor's `matchKey` format changes no earlier than 4 November 2026. Do not compare keys across that date.
- The UK Actor's default retailers change no earlier than 7 November 2026. The examples name retailers explicitly, so they are unaffected.

## Licence

The code is MIT. See `LICENSE`.

Data returned by the Actors is not covered by the MIT licence. It stays under each Actor's terms.

Retailer, portal and vendor names are trademarks of their owners. They are used only to describe the data. This project is not affiliated with or endorsed by them.
