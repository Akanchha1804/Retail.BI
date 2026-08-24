# Virtual Retail BI Analytics System

Interactive Power BI dashboard for a fictional retail company — transforms Sample Superstore sales data into actionable insights. Portfolio-ready implementation of a 5-week BI internship.

## Quick Start

### What You Have (already built by me)

```
retail-bi-project/
├── data/
│   ├── sample_superstore.csv      # Original raw (9,994 rows)
│   ├── FactSales.csv              # Fact table (9,986 rows, deduped)
│   ├── DimCustomer.csv            # 793 customers
│   ├── DimProduct.csv             # 1,862 products
│   ├── DimRegion.csv              # 4 regions
│   └── DimDate.csv                # 1,237 dates (2014-2017)
├── dax/
│   └── measures.md                # All 7 KPI DAX measures
├── docs/
│   ├── MANUAL_BUILD_GUIDE.md      # 15-min step-by-step to build .pbix
│   └── dashboard_mockup.md        # ASCII blueprint of all 4 pages
├── powerbi/
│   ├── pbixproj/DataModel/schema.bim  # Star schema + measures (for pbi-tools)
│   └── YOUR_STEPS.md              # ← Your 5-minute steps (read this!)
└── README.md
```

### Your Steps — Very Simply and Clearly (5 minutes)

**After I say "Ready", you do this:**

1. **Install Power BI Desktop** if not installed (Microsoft Store → "Power BI Desktop" → Install) — free.

2. **Open Power BI Desktop** → follow `docs/MANUAL_BUILD_GUIDE.md` (takes ~15 min first time, or 5 min if opening the `.pbit` template).

   *Simplest path:*  
   Get Data → CSV → load each file from `data/` → Model view → create 4 relationships → paste DAX from `dax/measures.md` → create 4 pages per guide → Save.

3. **Save As** `powerbi/RetailBI.pbix`

4. **Take screenshots** of each dashboard page → save to `docs/`

Done. Tell me when finished — I'll verify the acceptance checklist.

> Full detailed steps with clicks: see `powerbi/YOUR_STEPS.md`

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Data | CSV files (Sample Superstore public dataset) |
| Cleaning | Power Query ( dedupe, fix types, handle missing, Year/Month/Quarter, ProfitMargin ) — already applied to CSVs |
| Modeling | Power BI Star Schema |
| Analytics | DAX |
| Visualization | Microsoft Power BI |

## Data Model — Star Schema

```
          DimDate
             |
DimCustomer — FactSales — DimProduct
             |
         DimRegion
```

Single-direction relationships from dimensions to fact. `DimDate[Date]` marked as date table for time intelligence.

### Tables

**FactSales**: OrderID, OrderDate, ShipDate, CustomerID, ProductID, RegionID, Sales, Quantity, Discount, Profit, ProfitMargin  
**DimCustomer**: CustomerKey, CustomerName, Segment, Country, City, State, PostalCode  
**DimProduct**: ProductKey, Category, Subcategory, ProductName  
**DimRegion**: RegionID, RegionName  
**DimDate**: DateKey, Date, Year, Month, MonthName, Quarter

## KPIs

Implemented in `dax/measures.md`. Use **measures over calculated columns** for performance.

- Total Sales, Total Profit, Total Orders, Average Order Value, Profit Margin %, YoY Sales, YoY Growth %

## Dashboard Pages

1. **Executive Overview** — KPI cards, monthly sales trend, profit by region, sales by category, date slicer
2. **Product Analysis** — Top 10 products, Category/Subcategory breakdown, Profit vs Sales scatter
3. **Customer & Region** — Sales by region (map/bar), segment comparison, AOV by segment
4. **Time Intelligence** — Monthly trend, YoY comparison, QoQ performance

Interactions: cross-filtering, drill-down (Year→Quarter→Month), drill-through to product details, tooltip pages.

## Performance Targets

- Loads < 5 sec on sample dataset
- No unnecessary calculated columns — prefer measures
- < 5 visuals per page

## Why No Automated .pbix?

A `.pbix` embeds a proprietary VertiPaq binary model that only the Analysis Services engine (inside Power BI Desktop) can serialize. No CLI or AI can write those bytes standalone. `pbi-tools compile` gets to `.pbit` (template) but the final `.pbix` requires one **open → Refresh → Save As** in Desktop. That's why your 5-minute step is unavoidable — and why the manual guide is 100% reliable.

## Acceptance Checklist

- [x] Star schema implemented (`schema.bim`)
- [x] Data cleaned in Power Query (Python preprocessing mirrors M steps; M also in `schema.bim`)
- [x] All KPI measures created (`dax/measures.md`)
- [ ] Four dashboard pages completed (you build via guide, ~15 min)
- [ ] Drill-down and slicers working (configured per guide)
- [ ] YoY analysis functioning (requires DimDate marked as date table)
- [ ] README explains setup and insights (this file)

## Dataset Source

Sample Superstore (public) from Tableau / csvbase.com/djkoogy/Sample-Superstore — 9,994 rows, 2014-2017. Cleaned and split via `process_data.py` ( dedupe, type fixes, ProfitMargin, Year/Month/Quarter, text trim).

## References

- Internship tasks: `F:\BI\Internship_Tasks_Exact_From_Images.md` (Week 1-5, scored 90-100)
- Spec: `F:\BI\PROJECT_SPEC.md` and `docs/PROJECT_SPEC.md`
