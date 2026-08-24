import urllib.request
import csv
import os

# Download the raw CSV
url = 'https://csvbase.com/djkoogy/Sample-Superstore.csv'
with urllib.request.urlopen(url) as response:
    data = response.read().decode('utf-8')

# Save raw CSV
raw_path = r'F:\BI\retail-bi-project\data\raw_superstore.csv'
with open(raw_path, 'w', encoding='utf-8-sig') as f:
    f.write(data)
print(f'Saved raw CSV: {os.path.getsize(raw_path)} bytes')

# Read and process
rows = []
with open(raw_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f'Total rows: {len(rows)}')

# Create FactSales
fact_rows = []
seen = set()
for row in rows:
    order_id = row['Order ID']
    order_date = row['Order Date']
    ship_date = row['Ship Date']
    customer_id = row['Customer ID']
    product_id = row['Product ID']
    region = row['Region']
    try:
        sales = float(row['Sales']) if row['Sales'] else 0
        quantity = int(float(row['Quantity'])) if row['Quantity'] else 0
        discount = float(row['Discount']) if row['Discount'] else 0
        profit = float(row['Profit']) if row['Profit'] else 0
    except:
        continue
    if not order_id or not customer_id or not product_id:
        continue
    key = (order_id, product_id)
    if key in seen:
        continue
    seen.add(key)
    fact_rows.append({
        'OrderID': order_id,
        'OrderDate': order_date,
        'ShipDate': ship_date,
        'CustomerID': customer_id,
        'ProductID': product_id,
        'RegionID': region,
        'Sales': sales,
        'Quantity': quantity,
        'Discount': discount,
        'Profit': profit
    })

# Write FactSales CSV
fact_path = r'F:\BI\retail-bi-project\data\FactSales.csv'
with open(fact_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['OrderID','OrderDate','ShipDate','CustomerID','ProductID','RegionID','Sales','Quantity','Discount','Profit'])
    writer.writeheader()
    writer.writerows(fact_rows)
print(f'Wrote FactSales.csv: {len(fact_rows)} rows')

# Create DimCustomer: unique customers
cust_rows = []
cust_keys = set()
# Build lookup of customer data from original rows
cust_lookup = {}
for row in rows:
    cid = row['Customer ID']
    if cid not in cust_lookup:
        cust_lookup[cid] = row

for rf in fact_rows:
    cid = rf['CustomerID']
    if cid not in cust_keys:
        cust_keys.add(cid)
        orig = cust_lookup[cid]
        cust_rows.append({
            'CustomerKey': cid,
            'CustomerName': orig['Customer Name'],
            'Segment': orig['Segment'],
            'Country': orig['Country'],
            'City': orig['City'],
            'State': orig['State'],
            'PostalCode': orig['Postal Code']
        })

cust_path = r'F:\BI\retail-bi-project\data\DimCustomer.csv'
with open(cust_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['CustomerKey','CustomerName','Segment','Country','City','State','PostalCode'])
    writer.writeheader()
    writer.writerows(cust_rows)
print(f'Wrote DimCustomer.csv: {len(cust_rows)} rows')

# Create DimProduct: unique products
prod_rows = []
prod_keys = set()
prod_lookup = {}
for row in rows:
    pid = row['Product ID']
    if pid not in prod_lookup:
        prod_lookup[pid] = row

for rf in fact_rows:
    pid = rf['ProductID']
    if pid not in prod_keys:
        prod_keys.add(pid)
        orig = prod_lookup[pid]
        prod_rows.append({
            'ProductKey': pid,
            'Category': orig['Category'],
            'Subcategory': orig['Sub-Category'],
            'ProductName': orig['Product Name']
        })

prod_path = r'F:\BI\retail-bi-project\data\DimProduct.csv'
with open(prod_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['ProductKey','Category','Subcategory','ProductName'])
    writer.writeheader()
    writer.writerows(prod_rows)
print(f'Wrote DimProduct.csv: {len(prod_rows)} rows')

# Create DimRegion: distinct regions
region_vals = set()
for rf in fact_rows:
    region_vals.add(rf['RegionID'])

region_rows = [{'RegionID': r, 'RegionName': r} for r in sorted(region_vals)]
region_path = r'F:\BI\retail-bi-project\data\DimRegion.csv'
with open(region_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['RegionID','RegionName'])
    writer.writeheader()
    writer.writerows(region_rows)
print(f'Wrote DimRegion.csv: {len(region_rows)} rows')

# Create DimDate: date dimension from distinct order dates
date_set = set()
for rf in fact_rows:
    od = rf['OrderDate']
    if od:
        try:
            parts = od.split('-')
            if len(parts) == 3:
                year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            else:
                month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
            date_set.add((year, month, day))
        except:
            pass

date_rows = []
for y, m, d in sorted(date_set):
    month_name = f'Month {m:02d}'
    quarter = (m - 1) // 3 + 1
    date_rows.append({
        'DateKey': f'{y}{m:02d}{d:02d}',
        'OrderDate': f'{y}-{m:02d}-{d:02d}',
        'Year': y,
        'Month': m,
        'MonthName': month_name,
        'Quarter': quarter
    })

date_path = r'F:\BI\retail-bi-project\data\DimDate.csv'
with open(date_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['DateKey','OrderDate','Year','Month','MonthName','Quarter'])
    writer.writeheader()
    writer.writerows(date_rows)
print(f'Wrote DimDate.csv: {len(date_rows)} rows')

# Add ProfitMargin to FactSales rows
for rf in fact_rows:
    if rf['Sales'] != 0:
        rf['ProfitMargin'] = rf['Profit'] / rf['Sales']
    else:
        rf['ProfitMargin'] = 0

# Write updated FactSales with ProfitMargin
fact_path2 = r'F:\BI\retail-bi-project\data\FactSales.csv'
with open(fact_path2, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['OrderID','OrderDate','ShipDate','CustomerID','ProductID','RegionID','Sales','Quantity','Discount','Profit','ProfitMargin'])
    writer.writeheader()
    writer.writerows(fact_rows)
print(f'Wrote FactSales.csv with ProfitMargin: {len(fact_rows)} rows')

print('\nProcessing complete!')
print(f'FactSales: {len(fact_rows)} rows')
print(f'DimCustomer: {len(cust_rows)} customers')
print(f'DimProduct: {len(prod_rows)} products')
print(f'DimRegion: {len(region_rows)} regions')
print(f'DimDate: {len(date_rows)} dates')