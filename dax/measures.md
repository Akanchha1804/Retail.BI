# DAX Measures — Virtual Retail BI

All measures belong on `FactSales` unless noted. Mark `DimDate[Date]` as Date Table.

## Core KPIs (from PROJECT_SPEC.md)

```DAX
Total Sales = SUM(FactSales[Sales])

Total Profit = SUM(FactSales[Profit])

Total Orders = DISTINCTCOUNT(FactSales[OrderID])

Average Order Value =
DIVIDE([Total Sales], [Total Orders])

Profit Margin % =
DIVIDE([Total Profit], [Total Sales])

YoY Sales =
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(DimDate[Date])
)

YoY Growth % =
DIVIDE([Total Sales] - [YoY Sales], [YoY Sales])
```

## Extended Measures (for dashboard pages)

```DAX
-- Profit Margin per row already in FactSales[ProfitMargin] = Profit / Sales (use as column, but prefer measure above for aggregates)

Total Quantity = SUM(FactSales[Quantity])

Avg Discount = AVERAGE(FactSales[Discount])

Sales by Category (use as visual, not measure — drag DimProduct[Category])

Top 10 Products Sales =
CALCULATE(
    [Total Sales],
    TOPN(10, VALUES(DimProduct[ProductName]), [Total Sales])
)

-- Time Intelligence
QTD Sales = CALCULATE([Total Sales], DATESQTD(DimDate[Date]))
MTD Sales = CALCULATE([Total Sales], DATESMTD(DimDate[Date]))
Rolling 3M Avg = AVERAGEX(DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -3, MONTH), [Total Sales])

-- Customer / Region
Sales by Region = CALCULATE([Total Sales], ALLEXCEPT(DimRegion, DimRegion[RegionName]))
AOV by Segment =
CALCULATE([Average Order Value], ALLEXCEPT(DimCustomer, DimCustomer[Segment]))

-- Profit vs Sales scatter needs no extra measure — plot [Total Sales] vs [Total Profit] by Product
```

## Best Practices Applied
- Prefer **measures over calculated columns** (only ProfitMargin column kept for spec compliance — all aggregates are measures).
- Use `DIVIDE()` to avoid divide-by-zero.
- Single-direction relationships Dim → Fact (see schema).
- `DimDate[Date]` is continuous, marked as date table — required for SAMEPERIODLASTYEAR.
- Format `%` measures as Percentage, Sales/Profit as Currency.
