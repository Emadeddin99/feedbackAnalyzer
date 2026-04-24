import os
import matplotlib.pyplot as plt
from resolve_file import resolve_filename

PRODUCT_COLORS = [
    "#4C72B0",  # blue
    "#DD8452",  # orange
    "#55A868",  # green
    "#C44E52",  # red
    "#8172B2",  # purple
]


# --- Save Chart Image ---
def save_rating_chart(names, ratings, filename="VisualData/ratings_chart.png", show=True):
    """
    Generates a bar chart of average customer ratings by product and saves it.
    Returns early with a message if names/ratings lists are empty.
    Respects the user's file-conflict choice from resolve_filename.
    """
    if not names or not ratings:
        print("No chart data provided – chart not saved.")
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # --- Build chart ---
    fig, ax = plt.subplots(figsize=(10, 5))

    colors = [PRODUCT_COLORS[i % len(PRODUCT_COLORS)] for i in range(len(names))]
    bars   = ax.bar(names, ratings, color=colors)

    ax.set_title("Average Customer Ratings by Product")
    ax.set_xlabel("Product")
    ax.set_ylabel("Average Rating")
    ax.set_ylim(0, 5.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Label in the middle of each bar
    for bar, rating in zip(bars, ratings):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height() / 2
        ax.text(
            x, y, f"{rating:.1f}",
            ha="center", va="center",
            fontsize=11, fontweight="bold", color="white",
        )

    # --- Handle save decision ---
    resolved = resolve_filename(filename)
    if resolved is not None:
        plt.savefig(resolved)
        print(f"\nChart saved → {resolved}")
    else:
        print("Chart save cancelled.")

    if show:
        plt.show()

    plt.close()