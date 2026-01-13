def clean_sales_data(file_path):
    total_records = 0
    invalid_records = 0
    valid_records = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

    for line in lines[1:]:  # skip header
        line = line.strip()

        if not line:
            continue

        total_records += 1
        parts = line.split("|")

        if len(parts) != 8:
            invalid_records += 1
            continue

        transaction_id, date, product_id, product_name, quantity, price, customer_id, region = parts

        if not transaction_id.startswith("T"):
            invalid_records += 1
            continue

        if customer_id.strip() == "" or region.strip() == "":
            invalid_records += 1
            continue

        product_name = product_name.replace(",", "")
        quantity = quantity.replace(",", "")
        price = price.replace(",", "")

        try:
            quantity = int(quantity)
            price = float(price)
        except:
            invalid_records += 1
            continue

        if quantity <= 0 or price <= 0:
            invalid_records += 1
            continue

        valid_records.append([
    transaction_id,
    date,
    product_id,
    product_name,
    quantity,
    price,
    customer_id,
    region
])


    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records
