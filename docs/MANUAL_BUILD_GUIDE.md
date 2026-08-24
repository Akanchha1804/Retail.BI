# Manual Build Guide — RetailBI.pbix (15 minutes)

If `powerbi/RetailBI.pbit` fails to open, build from scratch following these exact steps. 100% reliable.

## Prereqs
- Install **Power BI Desktop** (Microsoft Store or https://powerbi.microsoft.com/desktop)
- Files ready in `F:\BI\retail-bi-project\data\`: `FactSales.csv` (9,986 rows), `DimCustomer.csv` (793), `DimProduct.csv` (1862), `DimRegion.csv` (4), `DimDate.csv` (1237)

---

## Step 1: Get Data (2 min)

1. Open Power BI Desktop → **Get Data** → **Text/CSV** → select `FactSales.csv` → **Load**
   - Repeat for `DimCustomer.csv`, `DimProduct.csv`, `DimRegion.csv`, `DimDate.csv`
2. You should see 5 tables in Fields pane.

### Power Query cleaning (already done in CSVs, but verify)
- **Home → Transform Data** → check each query:
  - Remove duplicates: already deduplicated on `(OrderID, ProductID)`
  - Data types: OrderDate/ShipDate/Date = Date, Sales/Profit/Discount = Decimal, Quantity = Whole Number
  - Year/Month/Quarter: already in `DimDate` (derived from OrderDate)
  - ProfitMargin: already in `FactSales` as `Profit / Sales`
- Click **Close & Apply**

---

## Step 2: Model — Star Schema (2 min)

1. Click **Model view** (left icon)
2. Drag to create relationships (all **single-direction**, cardinality as below). If auto-created, verify:
   - `DimCustomer[CustomerKey]` (1) → `FactSales[CustomerID]` (many) — active
   - `DimProduct[ProductKey]` (1) → `FactSales[ProductID]` (many) — active
   - `DimRegion[RegionID]` (1) → `FactSales[RegionID]` (many) — active
   - `DimDate[Date]` (1) → `FactSales[OrderDate]` (many) — active
3. Select `DimDate[Date]` → **Column tools → Mark as Date Table** → choose `Date` column
4. Diagram should look exactly like spec:
   ```
             DimDate
                |
   DimCustomer — FactSales — DimProduct
                |
            DimRegion
   ```

---

## Step 3: Create DAX Measures (3 min)

**Modeling → New Measure** (or right-click `FactSales` → New measure). Paste each from `dax/measures.md`:

```DAX
Total Sales = SUM(FactSales[Sales])
Total Profit = SUM(FactSales[Profit])
Total Orders = DISTINCTCOUNT(FactSales[OrderID])
Average Order Value = DIVIDE([Total Sales],[Total Orders])
Profit Margin % = DIVIDE([Total Profit],[Total Sales])
YoY Sales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))
YoY Growth % = DIVIDE([Total Sales]-[YoY Sales],[YoY Sales])
```

Format: select each measure → **Measure tools → Format** → `Total Sales`/`Total Profit` = Currency, `%` measures = Percentage, `Total Orders` = Whole Number.

---

## Step 4: Build 4 Report Pages (8 min)

### Page 1: Executive Overview
- Rename page to **Executive Overview**
- **Insert → Slicer** → `DimDate[Date]` (or Year/Month) — set to **Between** slicer
- **KPI cards** (Visual → Card): `Total Sales`, `Total Profit`, `Total Orders`, `Average Order Value`, `Profit Margin %`
- **Line chart** → Axis: `DimDate[Date]` (hierarchy: Year → Quarter → Month), Values: `Total Sales` — enable **Drill-down**
- **Bar chart** → Axis: `DimRegion[RegionName]`, Values: `Total Profit`
- **Donut/Bar** → Legend: `DimProduct[Category]`, Values: `Total Sales`
- Select all visuals → **Format → Edit interactions → Cross-filtering ON**

### Page 2: Product Analysis
- Rename to **Product Analysis**
- **Bar chart Top 10**: Axis `DimProduct[ProductName]`, Values `Total Sales`, Filters → Top N = 10 by `Total Sales`
- **Matrix or Bar**: Rows `DimProduct[Category]` → `Subcategory`, Values `Total Sales` + `Total Profit`
- **Scatter**: X = `Total Sales`, Y = `Total Profit`, Details = `DimProduct[ProductName]`, Size = `Total Quantity`
- Add **Drill-through**: Right-click page → Page information → Allow drill-through → drag `DimProduct[Category]` to drill-through filter

### Page 3: Customer & Region
- Rename to **Customer & Region**
- **Map or bar**: Location `DimCustomer[State]` or `DimRegion[RegionName]`, Values `Total Sales`
- **Bar**: Axis `DimCustomer[Segment]`, Values `Total Sales`
- **Card/Column**: `Average Order Value` by `DimCustomer[Segment]`

### Page 4: Time Intelligence
- Rename to **Time Intelligence**
- **Line**: `DimDate[Date]` (Month) vs `Total Sales`
- **Line with YoY**: `Total Sales` vs `YoY Sales` by `DimDate[Year]`
- **Bar/Matrix**: `DimDate[Quarter]` with `YoY Growth %` — conditional formatting red/green

---

## Step 5: Interactions & Polish (1 min)

- **Cross-filtering**: Select a visual → Format → Edit interactions → Filter/Cross-highlight as desired
- **Drill-down**: On Executive Overview line chart, enable drill-down buttons (Year → Quarter → Month)
- **Tooltip page**: Create new page → set **Allow use as tooltip** → add `ProductName`, `Total Sales`, `Profit Margin %`
- **Theme**: View → Themes → pick professional theme
- **Performance**: Keep < 5 visuals per page, use measures not calculated columns, hide unused columns (right-click → Hide)

---

## Step 6: Save & Verify

1. **File → Save As → `F:\BI\retail-bi-project\powerbi\RetailBI.pbix`**
2. Verify acceptance checklist:
   - [ ] Star schema implemented ✓
   - [ ] Data cleaned in Power Query ✓
   - [ ] All KPI measures created ✓
   - [ ] Four dashboard pages completed ✓
   - [ ] Drill-down and slicers working ✓
   - [ ] YoY analysis functioning ✓
   - [ ] Loads < 5 sec ✓
3. **Export screenshots**: File → Export → PDF or use Snipping Tool for `docs/` → `ExecutiveOverview.png` etc.

Done. You now have the deliverable `RetailBI.pbix`.
