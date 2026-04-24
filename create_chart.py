# This module contains a function to build chart data from the final_data dictionary.
def build_chart_data(final_data):
    """
    Extracts parallel lists of product names, average ratings, and profits
    from the final_data dict for use in charting functions.
    Returns three empty lists if final_data is empty or None.
    """
    if not final_data:
        return [], [], []

    names   = []
    ratings = []
    profits = []

    for item in final_data.values():
        names.append(item["product_name"])
        ratings.append(item["average_rating"])
        profits.append(item["profit"])

    return names, ratings, profits