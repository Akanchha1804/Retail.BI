# Dashboard Mockup — ASCII Blueprint

## Page 1: Executive Overview
```
+------------------------------------------------------------------+
| EXECUTIVE OVERVIEW                          [Date Slicer: 2014-2017]
+------------------------------------------------------------------+
| [Card: Total Sales]  [Card: Total Profit]  [Card: Total Orders]  [Card: AOV]  [Card: Margin %]  |
|  $2,297,200          $286,397               5,009                $458.6        12.47%           |
+------------------------------------------------------------------+
| Monthly Sales Trend (Line, drill Year→Q→Month)  | Profit by Region (Bar)      |
|  Sales ↑                                         | West |██████  $836k          |
|        /\                                        | East |████    $678k          |
|  -----/--\----/--\------                          | South|███     $391k          |
|      /    \/    \                                | Central|███   $389k          |
|  ------------------------------------------------|                            |
|  Sales by Category (Donut)                       |
|  Technology 37% | Furniture 32% | Office Supplies 31%                        |
+------------------------------------------------------------------+
```

## Page 2: Product Analysis
```
+------------------------------------------------------------------+
| PRODUCT ANALYSIS                                                 |
+------------------------------------------------------------------+
| Top 10 Products (Bar, desc by Sales)  | Category Breakdown          |
|  1. Canon imageCLASS 2200 ... $61k    |  Furniture: Bookcases etc   |
|  2. Fellowes PB500 ... $27k           |  Technology: Phones etc     |
|  ...                                 |  Office Supplies: Binders.. |
+------------------------------------------------------------------+
| Profit vs Sales Scatter (X=Sales, Y=Profit, size=Qty)              |
|  • High sales / high profit → stars                                |
|  • High sales / low profit → review discount strategy              |
+------------------------------------------------------------------+
```

## Page 3: Customer & Region
```
+------------------------------------------------------------------+
| CUSTOMER & REGION                                                |
+------------------------------------------------------------------+
| Sales by Region (Map/Bar)  | Customer Segment Comparison            |
|  West strongest, South weakest | Consumer 52% | Corporate 30% | Home Office 17% |
+------------------------------------------------------------------+
| AOV by Segment (Column)                                            |
|  Consumer $462 | Corporate $449 | Home Office $470                 |
+------------------------------------------------------------------+
```

## Page 4: Time Intelligence
```
+------------------------------------------------------------------+
| TIME INTELLIGENCE                                                |
+------------------------------------------------------------------+
| Monthly Trend (Line)              | YoY Comparison (Line: Sales vs YoY Sales)|
|  2014→2017 seasonal peaks Dec     |  2017 vs 2016 +20.4% growth             |
+------------------------------------------------------------------+
| Quarter-over-Quarter (Matrix + YoY Growth % with conditional color)|
|  Q1  Q2  Q3  Q4  | Growth green/red                              |
+------------------------------------------------------------------+
```

## Interactions
- **Cross-filtering**: Click any bar/segment → all visuals on page filter.
- **Drill-down**: Executive line chart Year → Quarter → Month.
- **Drill-through**: Right-click Product → drill to Product details.
- **Tooltip**: Hover product → shows Sales, Profit, Margin.
- **Slicers**: Date range slicer on Overview syncs to all pages (View → Sync slicers).
