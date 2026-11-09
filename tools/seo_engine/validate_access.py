"""Validate DataForSEO API credentials and verify exact NC city location_code IDs using free endpoints ($0.00 cost)."""
import os
import json
from dataforseo_client import DataForSEOClient, TARGET_LOCATIONS, DATA_DIR


def main():
    # budget_limit_usd=0.0 ensures zero paid API calls can run
    client = DataForSEOClient(budget_limit_usd=0.0, dry_run=False)
    print("Auth status:", client.check_credentials_status())

    user_data = client.request("/v3/appendix/user_data", None, method="GET")
    money = user_data["tasks"][0]["result"][0]["money"]
    print(f"Verified DataForSEO Balance: ${money.get('balance'):.4f} USD")

    locs = client.request("/v3/serp/google/locations/us", None, method="GET")
    all_locs = locs["tasks"][0]["result"]
    nc_locs = {
        l["location_name"]: l
        for l in all_locs
        if ",North Carolina,United States" in (l.get("location_name") or "")
    }
    print(f"Total North Carolina locations in DataForSEO geo table: {len(nc_locs)}")

    verified_locations = {}
    for k, v in TARGET_LOCATIONS.items():
        target_name = v["serp_location_name"]
        match = nc_locs.get(target_name)
        if match:
            verified_locations[k] = {
                "supported_directly": True,
                "location_code": match["location_code"],
                "location_name": match["location_name"],
                "location_type": match["location_type"],
                "coordinates": v["coordinates"],
            }
            print(
                f"  [SUPPORTED] {k:18} -> location_code={match['location_code']} "
                f"({match['location_name']} | {match['location_type']})"
            )
        else:
            partials = [
                (p["location_code"], p["location_name"], p["location_type"])
                for name, p in nc_locs.items()
                if v["city"].lower() in name.lower()
            ]
            fb_match = nc_locs.get(v["fallback_location_name"])
            verified_locations[k] = {
                "supported_directly": False,
                "requested_name": target_name,
                "partials": partials,
                "fallback_location_code": fb_match["location_code"] if fb_match else None,
                "fallback_location_name": v["fallback_location_name"],
                "coordinates": v["coordinates"],
            }
            print(f"  [FALLBACK]  {k:18} -> partials={partials}, fallback={v['fallback_location_name']}")

    out_path = os.path.join(DATA_DIR, "verified_nc_locations.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "account_balance_usd": money.get("balance"),
                "verified_locations": verified_locations,
            },
            f,
            indent=2,
        )


if __name__ == "__main__":
    main()
