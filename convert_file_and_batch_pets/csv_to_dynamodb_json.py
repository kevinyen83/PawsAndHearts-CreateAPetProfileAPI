import csv
import json
import sys

def csv_to_dynamodb_json(csv_file, json_file, table_name):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        items = []
        for row in reader:
            item = {"PutRequest": {"Item": {}}}
            for key, value in row.items():
                item["PutRequest"]["Item"][key] = {"S": value}
            items.append(item)

    with open(json_file, 'w') as jsonfile:
        json.dump({table_name: items}, jsonfile, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python csv_to_dynamodb_json.py <csv_file> <json_file> <table_name>")
        sys.exit(1)

    csv_file = sys.argv[1]
    json_file = sys.argv[2]
    table_name = sys.argv[3]
    csv_to_dynamodb_json(csv_file, json_file, table_name)
