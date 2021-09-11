import csv


def store_data(fields: list, bot_version: str):
    with open(f"runs_{bot_version}.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
