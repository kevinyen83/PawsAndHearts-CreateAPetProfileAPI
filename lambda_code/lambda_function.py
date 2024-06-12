import os
import json
import boto3
import base64
import uuid
from datetime import datetime

S3_BUCKET = os.environ.get('S3_BUCKET', 'pet-profile-image-bucket')
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'pet-table')

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
s3_client = boto3.client('s3', region_name='ap-southeast-2')

class PetInput:
    def __init__(self, organizationName, applicantName, contactEmail, contactPhone, petId, name, category, age, gender, color, size, location, vaccination, availability, image, description):
        self.organizationName = organizationName
        self.applicantName = applicantName
        self.contactEmail = contactEmail
        self.contactPhone = contactPhone
        self.petId = petId
        self.name = name
        self.category = category
        self.age = age
        self.gender = gender
        self.color = color
        self.size = size
        self.location = location
        self.vaccination = vaccination
        self.availability = availability
        self.image = image
        self.description = description

class PetType:
    def __init__(self, organizationName, applicantName, contactEmail, contactPhone, petId, name, category, age, gender, color, size, location, vaccination, availability, image, description):
        self.organizationName = organizationName
        self.applicantName = applicantName
        self.contactEmail = contactEmail
        self.contactPhone = contactPhone
        self.petId = petId
        self.name = name
        self.category = category
        self.age = age
        self.gender = gender
        self.color = color
        self.size = size
        self.location = location
        self.vaccination = vaccination
        self.availability = availability
        self.image = image
        self.description = description

class Query:
    @staticmethod
    def pet(petId):
        try:
            response = table.get_item(Key={'petId': petId})
            if 'Item' in response:
                return PetType(**response['Item'])
            else:
                return None
        except Exception as e:
            print(f"Error getting pet: {str(e)}")
            return None

    @staticmethod
    def pets():
        try:
            response = table.scan()
            if 'Items' in response:
                return [PetType(**item) for item in response['Items']]
            else:
                return []
        except Exception as e:
            print(f"Error getting pets: {str(e)}")
            return []

def lambda_handler(event, context):
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Request body is missing'})
        }

    body = json.loads(event['body'])
    try:
        pet_profile_data = create_pet_profile(body['variables']['petProfileData'])
        print('Pet profile created:', pet_profile_data)
        return {
            'statusCode': 200,
            'body': json.dumps({'data': {'createPetProfile': {'pet': pet_profile_data}}})
        }
    except Exception as e:
        error_message = str(e)
        if error_message.startswith('Missing required fields'):
            required_fields = [
                'contactEmail', 'contactPhone', 'organizationName', 'applicantName',
                'petId', 'name', 'category', 'age', 'gender', 'color', 'size',
                'location', 'vaccination', 'availability', 'image', 'description'
            ]
            missing_fields = [field for field in required_fields if field not in body['variables']['petProfileData']]
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Failed to create pet profile: Missing required fields', 'missing_fields': missing_fields})
            }
        else:
            print(f"Error creating pet profile: {error_message}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Failed to create pet profile: {error_message}'})
            }

def create_pet_profile(data):
    data['uploadDate'] = datetime.utcnow().isoformat()
    print("Pet profile data:", data)

    image_data = base64.b64decode(data['image'])
    print("Image data:", data['image'])

    image_id = str(uuid.uuid4())
    s3_key = f"{image_id}.jpg"

    try:
        print(f"Uploading image to S3: Bucket={S3_BUCKET}, Key={s3_key}")
        s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=image_data, ContentType='image/jpeg')
        image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"
        data['image'] = image_url
        print(f"Saving pet profile to DynamoDB: Table={DYNAMODB_TABLE_NAME}")
        table.put_item(Item=data)
        return data
    except Exception as e:
        print(f"Error creating pet profile: {str(e)}")
        raise Exception('Error creating pet profile')