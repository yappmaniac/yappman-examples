# 04 Leeds property listings with planning data, mapped

Searches Rightmove and Zoopla for homes for sale in Leeds. Each listing comes back with official planning constraints at its coordinates (England only) and planning applications within 150 metres from the last year. The notebook maps every listing and colours it by what was found.

- Actor: [UK Property Listings + Planning](https://apify.com/yappman/uk-property-listings) (`yappman/uk-property-listings`)
- Data: https://data.yappman.com

## How to run

1. Set up the environment as described in the root README, with `APIFY_TOKEN` set.
2. Open `leeds_property_planning_map.ipynb` in Jupyter Lab and run all cells.

## Actor input

```json
{
  "mode": "search",
  "portals": ["rightmove", "zoopla"],
  "locations": ["Leeds"],
  "listingType": "for-sale",
  "maxItems": 20,
  "includePlanningConstraints": true,
  "includePlanningApplications": true,
  "planningRadiusMetres": 150,
  "planningYears": 1
}
```

`maxItems` is shared across both portals. The run passes `max_total_charge_usd=0.37`.

## Cost (Free tier)

| Event | Count | Unit price | Most |
|---|---|---|---|
| Listing | 20 | $0.003 | $0.06 |
| Planning constraints | 20 | $0.005 | $0.10 |
| Planning applications | 20 | $0.01 | $0.20 |
| Run start | 1 | $0.005 | $0.005 |
| Total | | | $0.365 |

Constraints are charged only when the lookup succeeds. Applications are not charged for areas PlanIt does not cover.

## How the analysis works

- A constraint counts as present when its value is not null, false, empty string, empty list or empty dict. Flood zone values are shown as the zone number.
- Each listing is flattened to portal, address, price, beds, property type, coordinates, URL, present constraints, applications and `applicationsCoverage`.
- Likely duplicates are flagged in `possibleDuplicate`, not removed. A duplicate has the same latitude and longitude (rounded to 4 decimal places), price and bedrooms. The same home can appear on both portals.
- Marker colours:
  - Red: at least one planning constraint.
  - Orange: no constraints, but planning applications nearby.
  - Blue: neither.
- Each marker has a popup with address, price, beds, portal, listing link, constraints, and up to five applications (with a count of any more).

## Output

| File | Contents |
|---|---|
| `output/leeds_planning_applications.csv` | One row per nearby application (not written if there are none) |
| `output/leeds_map.html` | The map |

## Caveats

- Constraints cover England only.
- Planning applications come from a nightly copy of PlanIt. Check `applicationsCoverage` before reading "no applications" as "nothing planned".
- Listing data follows the Actor's data terms, not the repository's MIT licence.
