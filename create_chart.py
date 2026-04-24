# This module contains a function to build chart data from the final_data dictionary.
def build_chart_data(final_data):
    names = []
    ratings = []
    profits = []

    # Loop through the final_data dictionary and extract product names, average ratings, and profits for charting.
    for item in final_data.values():
        names.append(item["product_name"])
        ratings.append(item["average_rating"])
        profits.append(item["profit"])

    return names, ratings, profits