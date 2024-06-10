import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('pet-table')

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def convert_dynamodb_json(dynamodb_json):
    return {k: list(v.values())[0] for k, v in dynamodb_json.items()}

def extract_valid_items(data):
    batch_items = []
    for item in data['pet-table']:
        try:
            put_request = item['PutRequest']
            item_data = put_request['Item']
            if 'petId' in item_data:
                converted_item = convert_dynamodb_json(item_data)
                batch_items.append(converted_item)
            else:
                print(f"Missing petId in item: {item}")
        except KeyError as e:
            print(f"Invalid item structure: {item} - Missing key: {e}")
    return batch_items

def batch_write(items):
    with table.batch_writer() as batch:
        for item in items:
            print(f"Writing item: {item}")
            batch.put_item(Item=item)

def main():
    data = load_data('pets-data.json')
    batch_items = extract_valid_items(data)

    for i in range(0, len(batch_items), 25):
        batch_write(batch_items[i:i + 25])

    print("Batch write operation completed successfully.")

if __name__ == "__main__":
    main()