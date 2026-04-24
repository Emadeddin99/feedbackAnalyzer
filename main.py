
"""

Author's: Emad, Michael,CSC230, Spring 2026
Version: 1.0
Date: 04/23/2026

This is the main entry point for the dashboard application. It orchestrates the data fetching, analysis, and visualization steps.
It imports functions from other modules to handle specific tasks like data fetching, dashboard building, JSON saving, and chart creation.
The main function executes the following steps:
1. Fetch feedback and product data from JSON files.
2. Build statistics from the feedback data.
3. Merge statistics with product data to create a final dashboard data structure.
4. Save the dashboard data to a JSON file.
5. Build chart data from the final dashboard data.
6. Save a chart image based on the ratings data.
The script is designed to be run as a standalone program, and it will print the dashboard summary to the console and save the outputs to files.
"""


from data_analyze import fetchdata, build_and_print_dashboard
from save_to_json import save_dashboard
from create_chart import build_chart_data
from save_chart_image import save_rating_chart

def main(auto_save=True):

    fb_data = fetchdata("DATABASE/feedback.json")
    pr_data = fetchdata("DATABASE/product.json")

    if fb_data is None or pr_data is None:
        print("Data not available.")
        return

    # -------------------------
    # STEP 1: build stats
    # -------------------------
    stats = {}

    for entry in fb_data.values():
        pid = entry["product_id"]
        rating = entry["rating"]

        if pid not in stats:
            stats[pid] = {"count": 0, "total": 0, "comments": []}

        stats[pid]["count"] += 1
        stats[pid]["total"] += rating
        stats[pid]["comments"].append(entry["comment"])

    # -------------------------
    # STEP 2: use YOUR function (this replaces manual merge!)
    # -------------------------
    final_data = build_and_print_dashboard(stats, pr_data)

    # -------------------------
    # STEP 3: save JSON output
    # -------------------------
    save_dashboard(final_data)

    # -------------------------
    # STEP 4: build chart data
    # -------------------------
    names, ratings, profits = build_chart_data(final_data)

    # -------------------------
    # STEP 5: save chart
    # -------------------------
    if auto_save:
        save_rating_chart(names, ratings)

    print("\nDashboard generation complete.")


if __name__ == "__main__":
    main()