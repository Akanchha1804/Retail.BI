# PROJECT_SPEC.md

# Virtual Retail BI Analytics System

A portfolio-ready Business Intelligence project that reproduces the internship as a working implementation.

## Goal

Build an interactive Power BI dashboard for a fictional retail company that turns sales data into actionable business insights.

---

# Tech Stack

| Layer | Technology |
|---|---|
| Data | CSV files |
| Cleaning | Power Query |
| Modeling | Power BI star schema |
| Analytics | DAX |
| Visualization | Microsoft Power BI |

---

# Dataset

Use the **Sample Superstore** dataset (public) or an equivalent retail sales dataset with these tables.

### FactSales

- OrderID
- OrderDate
- ShipDate
- CustomerID
- ProductID
- RegionID
- Sales
- Quantity
- Discount
- Profit

### Dimensions

- DimCustomer
- DimProduct
- DimRegion
- DimDate

Create relationships using surrogate keys where appropriate.

---

# Data Model

Implement a **star schema**.

```text
          DimDate
             |
DimCustomer — FactSales — DimProduct
             |
         DimRegion
```

Single-direction relationships from dimensions to the fact table.

---

# Data Preparation

Power Query steps:

1. Remove duplicates
2. Fix data types
3. Handle missing values
4. Create Year, Month, Quarter columns
5. Standardize text fields
6. Create Profit Margin column

---

# KPIs

Implement these DAX measures.

```DAX
Total Sales = SUM(FactSales[Sales])

Total Profit = SUM(FactSales[Profit])

Total Orders = DISTINCTCOUNT(FactSales[OrderID])

Average Order Value =
DIVIDE([Total Sales],[Total Orders])

Profit Margin % =
DIVIDE([Total Profit],[Total Sales])

YoY Sales =
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(DimDate[Date])
)

YoY Growth % =
DIVIDE([Total Sales]-[YoY Sales],[YoY Sales])
```

---

# Dashboard Pages

## Executive Overview

- KPI cards
- Monthly sales trend
- Profit by region
- Sales by category
- Date slicer

## Product Analysis

- Top 10 products
- Category/Subcategory breakdown
- Profit vs Sales scatter plot

## Customer & Region

- Sales by region map or bar chart
- Customer segment comparison
- Average order value by segment

## Time Intelligence

- Monthly trend
- YoY comparison
- Quarter-over-quarter performance

---

# Interactions

Enable:

- Cross-filtering
- Drill-down (Year → Quarter → Month)
- Drill-through to product details
- Tooltip pages for product metrics

---

# Performance Targets

- Dashboard loads in under 5 seconds on the sample dataset
- No unnecessary calculated columns
- Prefer measures over calculated columns
- Minimize visual count per page

---

# Folder Structure

```text
retail-bi-project/
│
├── data/
│   └── sample_superstore.csv
├── docs/
│   ├── PROJECT_SPEC.md
│   └── dashboard_mockup.png
├── powerbi/
│   └── RetailBI.pbix
├── dax/
│   └── measures.md
└── README.md
```

---

# Acceptance Checklist

- [ ] Star schema implemented
- [ ] Data cleaned in Power Query
- [ ] All KPI measures created
- [ ] Four dashboard pages completed
- [ ] Drill-down and slicers working
- [ ] YoY analysis functioning
- [ ] README explains setup and insights

---

# Deliverables

1. `RetailBI.pbix`
2. Cleaned CSV dataset
3. `README.md`
4. `PROJECT_SPEC.md`
5. Dashboard screenshots
