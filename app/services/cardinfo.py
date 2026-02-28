import io
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server use
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def card_statistics(soldlistings):
   prices = [item["price"] for item in soldlistings]
   prices.sort()
   min_price = prices[0]
   max_price = prices[-1]
   avg = sum(prices) / len(prices)
   median = prices[len(prices)//2]
   trend = "Stable" # Default value
   if median > avg:
         trend = "Stable"
   elif median < avg:
         trend = "Falling"
   if min_price is None or max_price is None or avg is None or median is None or trend is None:
       return {"message": "Insufficient data to calculate statistics"}
   return {"message": "Statistics calculated", "min": min_price, "max": max_price, "mean": avg, "trend": trend}


def generate_price_date_plot(soldlistings, card_name="Card"):
    """Generate a scatter plot of sold date vs sold price and return it as PNG bytes."""
    dates = []
    prices = []
    for item in soldlistings:
        if item.get("date") and item.get("price") is not None:
            try:
                dt = datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
                dates.append(dt)
                prices.append(item["price"])
            except (ValueError, TypeError):
                continue

    if not dates:
        return None

    paired = sorted(zip(dates, prices), key=lambda x: x[0])
    dates, prices = zip(*paired)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(dates, prices, alpha=0.7, edgecolors="black", linewidth=0.5, c="#3b82f6")

    date_nums = mdates.date2num(dates)
    if len(date_nums) >= 2:
        z = np.polyfit(date_nums, prices, 1)
        p = np.poly1d(z)
        ax.plot(dates, p(date_nums), "--", color="#ef4444", linewidth=2, label="Trend")
        ax.legend()

    ax.set_title(f"Sold Price vs Date — {card_name}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Sold Date")
    ax.set_ylabel("Price ($)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()