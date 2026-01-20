from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from utils.report_generator import generate_sales_report


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read data
        print("\n[1/10] Reading sales data...")
        raw = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw)} records")

        # 2. Parse
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw)
        print(f"✓ Parsed {len(transactions)} transactions")

        # 3. Filter options
        print("\n[3/10] Filter Options Available:")
        print("Regions: North, South, East, West")
        print("Amount Range: ₹500 - ₹900,000")

        choice = input("Do you want to filter data? (y/n): ").lower()

        if choice == "y":
            region = input("Enter region (or press Enter to skip): ") or None
            min_amt = input("Min amount (or press Enter): ")
            max_amt = input("Max amount (or press Enter): ")
            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None
        else:
            region = min_amt = max_amt = None

        # 4. Validate
        print("\n[4/10] Validating transactions...")
        valid_tx, invalid, summary = validate_and_filter(
            transactions, region, min_amt, max_amt
        )
        print(f"✓ Valid: {len(valid_tx)} | Invalid: {invalid}")

        # 5. Analysis
        print("\n[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_tx)
        regions = region_wise_sales(valid_tx)
        top_products = top_selling_products(valid_tx)
        customers = customer_analysis(valid_tx)
        trend = daily_sales_trend(valid_tx)
        peak_day = find_peak_sales_day(valid_tx)
        low_products = low_performing_products(valid_tx)
        print("✓ Analysis complete")

        # 6. API
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_map = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrichment
        print("\n[7/10] Enriching sales data...")
        enriched = enrich_sales_data(valid_tx, product_map)
        success = sum(1 for t in enriched if t["API_Match"])
        print(f"✓ Enriched {success}/{len(enriched)} transactions")

        # 8. Save enriched
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched)
        print("✓ Saved to output/enriched_sales_data.txt")

        # 9. Report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched)
        print("✓ Report saved to output/sales_report.txt")

        # 10. Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ ERROR:", str(e))


if __name__ == "__main__":
    main()
