import csv
from datetime import date, timedelta

path = r"F:\BI\retail-bi-project\data\DimDate.csv"

with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print("OLD rows:", len(rows))
print("OLD min:", rows[0]["OrderDate"], "| max:", rows[-1]["OrderDate"])

have = set(r["OrderDate"] for r in rows)
d = date.fromisoformat(min(have))
end = date.fromisoformat(max(have))
missing = []
while d <= end:
    if d.isoformat() not in have:
        missing.append(d.isoformat())
    d += timedelta(days=1)
print("Gaps inside old range:", len(missing), "| examples:", missing[:5])
print("Duplicates:", len(rows) - len(have))

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

start = date(2014, 1, 1)
stop = date(2017, 12, 31)

with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["DateKey", "Date", "Year", "Month", "MonthName", "Quarter"])
    d = start
    n = 0
    while d <= stop:
        w.writerow([d.strftime("%Y%m%d"), d.isoformat(), d.year,
                    d.month, months[d.month - 1], (d.month - 1) // 3 + 1])
        n += 1
        d += timedelta(days=1)

with open(path, newline="", encoding="utf-8") as f:
    out = list(csv.reader(f))
print("NEW rows:", len(out) - 1)
print("NEW header:", ",".join(out[0]))
print("NEW first:", ",".join(out[1]))
print("NEW last :", ",".join(out[-1]))

newdates = [r[1] for r in out[1:]]
assert len(newdates) == len(set(newdates)), "duplicate dates!"
s = date.fromisoformat(newdates[0])
e = date.fromisoformat(newdates[-1])
assert (e - s).days + 1 == len(newdates), "still has gaps!"
print("CONTIGUOUS: OK")
