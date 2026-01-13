def analyze_sales_data(cleaned_data):
    total_revenue = 0
    sales_by_region = {}
    sales_by_product = {}

    for record in cleaned_data:
        transaction_id, date, product_id, product_name, quantity, price, customer_id, region = record

        revenue = quantity * price
        total_revenue += revenue

        if region not in sales_by_region:
            sales_by_region[region] = 0
        sales_by_region[region] += revenue

        if product_name not in sales_by_product:
            sales_by_product[product_name] = 0
        sales_by_product[product_name] += revenue

    top_product = max(sales_by_product, key=sales_by_product.get)

    return {
        "total_revenue": total_revenue,
        "sales_by_region": sales_by_region,
        "top_product": top_product
    }
