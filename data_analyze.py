import json
import os  # for terminal width and file handling


# --- Fetch Data ---
def fetchdata(filename):
    """
    Reads a JSON file and returns its contents as a Python dictionary.
    Handles file-not-found and JSON decode errors by printing an error
    message and returning None (no GUI dependency).
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: '{filename}' contains invalid JSON.")
    return None


# --- Build and Print Dashboard ---
def build_and_print_dashboard(stats, pr_data):
    """
    Merges aggregated feedback stats with product metadata.
    Prints a formatted dashboard to the console and returns final_data dict.
    """

    final_data = {}

    for product_id, data in stats.items():

        product = pr_data.get(product_id)

        if not product:
            print(f"Warning: product_id '{product_id}' found in feedback but missing from product data. Skipping.")
            continue

        price  = product["retail_price"]
        cost   = product["cost_to_produce"]
        count  = data["count"]

        avg_rating = data["total"] / count
        revenue    = price * count
        profit     = (price - cost) * count

        final_data[product_id] = {
            "product_name":    product["product_name"],
            "retail_price":    round(price, 2),
            "cost_to_produce": round(cost, 2),
            "count":           count,
            "average_rating":  round(avg_rating, 1),
            "revenue":         round(revenue, 2),
            "profit":          round(profit, 2),
            "sample_comments": data.get("comments", [])[:2],
        }

    if not final_data:
        print("No data to display in dashboard.")
        return final_data

    # Guard against non-terminal environments (piped output, CI, etc.)
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80

    title   = "DASHBOARD SUMMARY"
    padding = (width - len(title) - 2) // 2
    print("\n" + "=" * padding + " " + title + " " + "=" * padding + "\n")

    for pid, item in final_data.items():

        comment_preview = ""
        if item["sample_comments"]:
            comment_preview = f" | Comment: {item['sample_comments'][0]}"

        output = (
            f"{item['product_name']} | "
            f"Price: ${item['retail_price']:.2f} | "
            f"Sold: {item['count']} | "
            f"Avg: {item['average_rating']:.1f} | "
            f"Profit: ${item['profit']:.2f}"
            f"{comment_preview}"
        )

        print(output.center(width))
        print(("-" * len(output)).center(width))

    return final_data