import csv

fields = ["first", "second", "third"]
with open(r"name", "a") as f:
    writer = csv.writer(f)
    writer.writerow(fields)
