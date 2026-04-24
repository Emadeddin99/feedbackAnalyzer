import json
from tkinter import messagebox
import os #for terminal width and file handling
import random


# --- Fetch Data ---
def fetchdata(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
        
    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"{filename} is invalid.")
    return None

#fetchdata function reads a JSON file and returns its contents as a Python dictionary. It handles file not found and JSON decode errors by showing an error message box and returning None.
def fetch_values(table, field):
    if not table:
        return []

    return [entry.get(field) for entry in table.values() if entry.get(field) is not None]#fetch values from a specific field in a table (dict of dicts) and return as a list, filtering out None values

# --- Build and Print Dashboard ---
def build_and_print_dashboard(stats, pr_data):

    #store final data in a new dict
    final_data = {}

    #loop through stats and merge with product data
    for product_id, data in stats.items():

        product = pr_data.get(product_id)#get product info from pr_data using product_id

        if not product:#if product info is missing, skip and print warning
            print(f"Missing product: {product_id}")#print warning and skip if product info is missing
            continue#if product info is missing, skip and print warning

        price = product["retail_price"]#get retail price from product info
        cost = product["cost_to_produce"]#get cost to produce from product info
        count = data["count"]#get count of ratings from stats data

        avg_rating = data["total"] / count#calculate average rating by dividing total rating by count
        revenue = price * count#calculate revenue by multiplying price by count
        profit = (price - cost) * count#calculate profit by multiplying (price - cost) by count

        final_data[product_id] = {#store merged data in final_data dict using product_id as key
            "product_name": product["product_name"],#get product name from product info
            "retail_price": round(price, 2),#get retail price from product info
            "cost_to_produce": round(cost, 2),#get cost to produce from product info
            "count": count,#get count of ratings from stats data
            "average_rating": round(avg_rating, 1),#calculate average rating by dividing total rating by count
            "revenue": round(revenue, 2),#calculate revenue by multiplying price by count
            "profit": round(profit, 2),#calculate profit by multiplying (price - cost) by count

            # optional: keep comments but controlled
            "sample_comments": data.get("comments", [])[:2]
        }

    # --------------------------
    # PRINT DASHBOARD
    # --------------------------
    width = os.get_terminal_size().columns#get terminal width for centering output
    title = "DASHBOARD SUMMARY"#set dashboard title
    padding = (width - len(title) - 2) // 2  # -2 for spaces around title#
    print("\n" + "=" * padding + " " + title + " " + "=" * padding + "\n")#print dashboard title centered with padding

    for pid, item in final_data.items():#loop through final_data and print formatted output for each product

        comment_preview = ""#initialize comment preview as empty string
        if item["sample_comments"]:#if there are sample comments, add the first one to the preview
            comment_preview = f" | Comment: {item['sample_comments'][0]}"#add first sample comment to preview if available

        output = (#format output string with product name, price, count, average rating, profit, and optional comment preview
            f"{item['product_name']} | "#add product name to output
            f"Price: ${item['retail_price']:.2f} | "#add retail price to output formatted to 2 decimal places
            f"Sold: {item['count']} | "#add count of ratings (sold) to output
            f"Avg: {item['average_rating']:.1f} | "#add average rating to output formatted to 1 decimal place
            f"Profit: ${item['profit']:.2f}"#add profit to output formatted to 2 decimal places
            f"{comment_preview}"#add comment preview to output if available
        )

        print(output.center(width))#print formatted output centered in terminal
        k = "-" * len(output) #create a separator line of dashes with the same length as the output string
        print(k.center(width)) #print separator line centered in terminal

    return final_data #return final_data dict for further use (e.g., saving to JSON or creating charts)