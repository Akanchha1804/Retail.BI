import json, os, uuid, shutil, glob

ROOT = r"F:\BI\retail-bi-project\powerbi\RetailBI.Report\definition\pages"
VC = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.12.0/schema.json"

def fld(entity, prop, kind):
    return {kind: {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}

def proj(entity, prop, kind="Column"):
    return {"field": fld(entity, prop, kind), "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}

def mproj(measure, entity="FactSales"):
    return proj(entity, measure, "Measure")

def aggSum(entity, prop):
    return {
        "field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}, "Function": 0}},
        "queryRef": f"Sum({entity}.{prop})",
        "nativeQueryRef": f"Sum of {prop}"
    }

def visual(name, vtype, roles, pos, sort=None, tab=0):
    q = {"queryState": {r: {"projections": p} for r, p in roles.items()}}
    if sort:
        q["sortDefinition"] = {"sort": [{"field": sort["field"], "direction": sort["dir"]}], "isDefaultSort": True}
    return {
        "$schema": VC,
        "name": uuid.uuid4().hex,
        "position": {"x": pos[0], "y": pos[1], "z": 0, "width": pos[2], "height": pos[3], "tabOrder": tab},
        "visual": {"visualType": vtype, "query": q, "drillFilterOtherVisuals": True},
    }

M = lambda m: mproj(m)
MS = lambda m: fld("FactSales", m, "Measure")
C = lambda e, p: proj(e, p)

pages = {}

# ---------------- PAGE 1 : Executive Overview ----------------
p1 = []
p1.append(visual("slicerYear", "slicer", {"Values": [C("DimDate", "Year")]}, (16, 16, 360, 120)))
for i, m in enumerate(["Total Sales", "Total Profit", "Total Orders", "Average Order Value", "Profit Margin %"]):
    p1.append(visual(f"card{i}", "cardVisual", {"Data": [M(m)]}, (388 + i * 302, 16, 290, 120), tab=i + 1))
p1.append(visual("trendLine", "lineChart",
                 {"Category": [C("DimDate", "Date")], "Values": [M("Total Sales")]},
                 (16, 152, 1250, 600), tab=10))
p1.append(visual("catDonut", "donutChart",
                 {"Category": [C("DimProduct", "Category")], "Y": [M("Total Sales")]},
                 (1282, 152, 622, 290), tab=11))
p1.append(visual("regionBar", "barChart",
                 {"Category": [C("DimRegion", "RegionName")], "Y": [M("Total Profit")]},
                 (1282, 458, 622, 294),
                 sort={"field": MS("Total Profit"), "dir": "Descending"}, tab=12))
p1.append(visual("slicerDate", "slicer", {"Values": [C("DimDate", "Date")]}, (16, 768, 372, 110), tab=13))
pages["Executive Overview"] = ("745e2e52d0f540c67f70", p1)

# ---------------- PAGE 2 : Product Analysis ----------------
p2 = []
p2.append(visual("catMatrix", "matrix",
                 {"Rows": [C("DimProduct", "Category"), C("DimProduct", "Subcategory")],
                  "Values": [M("Total Sales"), M("Total Profit")]},
                 (16, 16, 900, 500)))
p2.append(visual("subcatBar", "barChart",
                 {"Category": [C("DimProduct", "Subcategory")], "Y": [M("Total Sales")]},
                 (932, 16, 972, 500),
                 sort={"field": MS("Total Sales"), "dir": "Descending"}))
p2.append(visual("scat", "scatterChart",
                 {"X": [M("Total Sales")], "Y": [M("Total Profit")],
                  "Size": [aggSum("FactSales","Quantity")], "Details": [C("DimProduct", "ProductName")]},
                 (16, 532, 1250, 532)))
p2.append(visual("topProdBar", "barChart",
                 {"Category": [C("DimProduct", "ProductName")], "Y": [M("Total Sales")]},
                 (1282, 532, 622, 532),
                 sort={"field": MS("Total Sales"), "dir": "Descending"}))
pages["Product Analysis"] = (uuid.uuid4().hex[:20], p2)

# ---------------- PAGE 3 : Customer & Region ----------------
p3 = []
p3.append(visual("stateBar", "barChart",
                 {"Category": [C("DimCustomer", "State")], "Y": [M("Total Sales")]},
                 (16, 16, 940, 520),
                 sort={"field": MS("Total Sales"), "dir": "Descending"}))
p3.append(visual("regionSalesBar", "barChart",
                 {"Category": [C("DimRegion", "RegionName")], "Y": [M("Total Sales")]},
                 (972, 16, 932, 250),
                 sort={"field": MS("Total Sales"), "dir": "Descending"}))
p3.append(visual("segBar", "barChart",
                 {"Category": [C("DimCustomer", "Segment")], "Y": [M("Total Sales")]},
                 (972, 282, 932, 254),
                 sort={"field": MS("Total Sales"), "dir": "Descending"}))
p3.append(visual("aovCol", "columnChart",
                 {"Category": [C("DimCustomer", "Segment")], "Y": [M("Average Order Value")]},
                 (16, 552, 940, 512)))
pages["Customer & Region"] = (uuid.uuid4().hex[:20], p3)

# ---------------- PAGE 4 : Time Intelligence ----------------
p4 = []
p4.append(visual("monthTrend", "lineChart",
                 {"Category": [C("DimDate", "Month")], "Values": [M("Total Sales")]},
                 (16, 16, 1888, 420)))
p4.append(visual("yoyLine", "lineChart",
                 {"Category": [C("DimDate", "Year")], "Values": [M("Total Sales"), M("YoY Sales")]},
                 (16, 452, 940, 612)))
p4.append(visual("qtrMatrix", "matrix",
                 {"Rows": [C("DimDate", "Quarter")],
                  "Values": [M("Total Sales"), M("YoY Growth %")]},
                 (972, 452, 930, 612)))
pages["Time Intelligence"] = (uuid.uuid4().hex[:20], p4)

# ---------------- CLEAN + WRITE ----------------
for d in glob.glob(os.path.join(ROOT, "*")):
    if os.path.isdir(d) or d.endswith("pages.json"):
        shutil.rmtree(d, ignore_errors=True) if os.path.isdir(d) else os.remove(d)

order = []
for disp, (pid, vis) in pages.items():
    pdir = os.path.join(ROOT, pid)
    os.makedirs(os.path.join(pdir, "visuals"), exist_ok=True)
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": pid, "displayName": disp, "displayOption": "FitToPage",
        "height": 1080, "width": 1920,
    }, open(os.path.join(pdir, "page.json"), "w"), indent=2)
    for v in vis:
        vdir = os.path.join(pdir, "visuals", v["name"])
        os.makedirs(vdir, exist_ok=True)
        json.dump(v, open(os.path.join(vdir, "visual.json"), "w"), indent=2)
    order.append(pid)

json.dump({
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
    "pageOrder": order,
    "activePageName": order[0],
}, open(os.path.join(ROOT, "pages.json"), "w"), indent=2)

print("Pages:", len(pages))
for d, (pid, vis) in pages.items():
    print(f"  {d} ({pid}) -> {len(vis)} visuals (folder-per-visual)")
