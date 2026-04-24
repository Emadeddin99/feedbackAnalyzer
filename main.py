"""
Author's: Emad, Michael, CSC230, Spring 2026
Version: 1.1
Date: 04/23/2026

Main entry point for the dashboard application.
Steps:
  1. Fetch feedback and product data from JSON files.
  2. Validate that all product_ids in feedback exist in the product catalogue.
  3. Build per-product statistics from the feedback data.
  4. Merge statistics with product data to create the final dashboard structure.
  5. Save the dashboard data to a JSON file.
  6. Build chart data and save a ratings chart image.
"""

from data_analyze import fetchdata, build_and_print_dashboard
from save_to_json import save_dashboard
from create_chart import build_chart_data
from save_chart_image import save_rating_chart


def validate_product_ids(fb_data, pr_data):
    """
    Check that every product_id referenced in feedback.json exists in
    product.json. Prints a warning for each orphaned ID and returns
    False if any are found so the caller can decide whether to abort.
    """
    unknown_ids = set()
    for entry in fb_data.values():
        pid = entry.get("product_id")
        if pid and pid not in pr_data:
            unknown_ids.add(pid)

    if unknown_ids:
        for pid in sorted(unknown_ids):
            print(f"Warning: product_id '{pid}' in feedback.json has no match in product.json.")
        return False   # caller receives False but we still continue (graceful degradation)

    return True


def main(auto_save=True):

    fb_data = fetchdata("DATABASE/feedback.json")
    pr_data = fetchdata("DATABASE/product.json")

    if fb_data is None or pr_data is None:
        print("Data not available. Exiting.")
        return

    # -------------------------
    # STEP 1: validate IDs
    # -------------------------
    validate_product_ids(fb_data, pr_data)   # warnings printed inside; we continue regardless

    # -------------------------
    # STEP 2: build stats
    # -------------------------
    stats = {}

    for entry in fb_data.values():
        pid    = entry.get("product_id")
        rating = entry.get("rating")

        # Skip malformed entries that are missing required fields
        if pid is None or rating is None:
            print(f"Warning: Skipping malformed feedback entry: {entry}")
            continue

        if pid not in stats:
            stats[pid] = {"count": 0, "total": 0, "comments": []}

        stats[pid]["count"]  += 1
        stats[pid]["total"]  += rating
        stats[pid]["comments"].append(entry.get("comment", ""))

    if not stats:
        print("No valid feedback entries found. Exiting.")
        return

    # -------------------------
    # STEP 3: build dashboard
    # -------------------------
    final_data = build_and_print_dashboard(stats, pr_data)

    if not final_data:
        print("Dashboard build produced no results. Exiting.")
        return

    # -------------------------
    # STEP 4: save JSON output
    # -------------------------
    save_dashboard(final_data)

    # -------------------------
    # STEP 5: build chart data
    # -------------------------
    names, ratings, profits = build_chart_data(final_data)

    # -------------------------
    # STEP 6: save chart
    # -------------------------
    if auto_save and names:
        save_rating_chart(names, ratings)
    elif not names:
        print("No chart data available – chart skipped.")

    print("\nDashboard generation complete.")


if __name__ == "__main__":
    main()