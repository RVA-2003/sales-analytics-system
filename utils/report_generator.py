from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [tx["date"] for tx in transactions if "date" in tx]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    region_sales = region_wise_sales(transactions)
    top_products = top_selling_products(transactions)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    api_matches = [tx for tx in enriched_transactions if tx.get("API_Match")]
    api_failures = [tx for tx in enriched_transactions if not tx.get("API_Match")]
    api_success_rate = (len(api_matches) / len(enriched_transactions) * 100) if enriched_transactions else 0

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 40 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {total_transactions}\n")
        f.write("=" * 40 + "\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        # REGION PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 40 + "\n")
        f.write("Region | Sales | % of Total | Transactions\n")
        for region, data in sorted(region_sales.items(), key=lambda x: x[1]["total_sales"], reverse=True):
            f.write(
                f"{region} | ₹{data['total_sales']:,.0f} | "
                f"{data['percentage']}% | {data['transaction_count']}\n"
            )
        f.write("\n")

        # TOP PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 40 + "\n")
        f.write("Rank | Product | Quantity | Revenue\n")
        for i, (product, qty, revenue) in enumerate(top_products, 1):
            f.write(f"{i} | {product} | {qty} | ₹{revenue:,.0f}\n")
        f.write("\n")

        # TOP CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        f.write("Rank | Customer | Total Spent | Orders\n")
        for i, (cid, info) in enumerate(list(customers.items())[:5], 1):
            f.write(
                f"{i} | {cid} | ₹{info['total_spent']:,.0f} | {info['purchase_count']}\n"
            )
        f.write("\n")

        # DAILY TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 40 + "\n")
        f.write("Date | Revenue | Transactions | Customers\n")
        for date, info in daily_trend.items():
            f.write(
                f"{date} | ₹{info['revenue']:,.0f} | "
                f"{info['transaction_count']} | {info['unique_customers']}\n"
            )
        f.write("\n")

        # PERFORMANCE INSIGHTS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Best Selling Day: {peak_day}\n")
        f.write("Low Performing Products:\n")
        for product in low_products:
            f.write(f"{product}\n")
        f.write("\n")

        # API SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Records Enriched: {len(api_matches)}\n")
        f.write(f"Success Rate: {api_success_rate:.2f}%\n")
        f.write("Failed Product IDs:\n")
        for tx in api_failures:
            f.write(f"{tx.get('ProductID')}\n")

    print("Sales report generated at:", output_file)
