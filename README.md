# Paws And Hearts-Pet Profile GraphQL API

![Alt text](https://github.com/kevinyen83/PawsAndHearts-AWSSAM-GraphQL-API/blob/main/screenshots/AWS.drawio.png)

## Introduction

This API is based on the Paws And Hearts project and provides a GraphQL interface for managing pet profiles. Users can create and read pet profiles through this interface. Please feel free to review the parent project: https://github.com/kevinyen83/PawsAndHearts

### Built With

![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

1.  Back-end development: Python
2.  API: GraphQL, Swagger
3.  AWS: CDK, CloudFormation, Lambda, API Gateway, DynamoDB, S3

## Endpoint

GraphQL Endpoint URL:

```sh
https://<your-api-id>.execute-api.<your-region>.amazonaws.com/Prod/pet
```

## Usage

### Swagger

For more details and to try out the API, please visit: https://kevinyen83.github.io/PawsAndHearts-AWSSAM-GraphQL-API/

### Create a Pet Profile

**Request**

- **URL**: `https://<your-api-id>.execute-api.<your-region>.amazonaws.com/Prod/pet`
- **Method**: `POST`
- **Headers**:
  - `Content-Type: application/json`
  - `x-api-key: <your-api-key>`

**Request Example**:

```
{
  "query": "mutation CreatePet($petProfileData: PetInput!) { createPetProfile(petProfileData: $petProfileData) { pet { petId organizationName applicantName contactEmail contactPhone name category age gender color size location vaccination availability image description } } }",
  "variables": {
    "petProfileData": {
      "organizationName": "Pet Rescue Org",
      "applicantName": "John Doe",
      "contactEmail": "johndoe@example.com",
      "contactPhone": "1234567890",
      "petId": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Buddy",
      "category": "Dog",
      "age": 3,
      "color": "Brown",
      "gender": "Male",
      "size": "Medium",
      "location": "New York, NY",
      "vaccination": "Yes",
      "availability": "Yes",
      "image": "http://example.com/buddy.jpg",
      "description": "A friendly and playful dog."
    }
  }
}
```

**Response Example**:

```
{
  "data": {
    "createPetProfile": {
      "pet": {
        "petId": "123e4567-e89b-12d3-a456-426614174000",
        "organizationName": "Pet Rescue Org",
        "applicantName": "John Doe",
        "contactEmail": "johndoe@example.com",
        "contactPhone": "1234567890",
        "name": "Buddy",
        "category": "Dog",
        "age": 3,
        "color": "Brown",
        "gender": "Male",
        "size": "Medium",
        "location": "New York, NY",
        "vaccination": "Yes",
        "availability": "Yes",
        "image": "http://example.com/buddy.jpg",
        "description": "A friendly and playful dog."
      }
    }
  }
}
```

## Data Model

### PetInput

```
input PetInput {
  organizationName: String!
  applicantName: String!
  contactEmail: String!
  contactPhone: String!
  petId: ID!
  name: String!
  category: String!
  age: Int!
  color: String!
  gender: String!
  size: String!
  location: String!
  vaccination: String!
  availability: String!
  image: String!
  description: String!
}
```

### Pet

```
type Pet {
  petId: ID!
  organizationName: String!
  applicantName: String!
  contactEmail: String!
  contactPhone: String!
  name: String!
  category: String!
  age: Int!
  color: String!
  gender: String!
  size: String!
  location: String!
  vaccination: String!
  availability: String!
  image: String!
  description: String!
}
```

## Error Handling

If the request fails, the response will contain error information. For example:

```
{
  "errors": [
    {
      "message": "Pet not found",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": [
        "pet"
      ]
    }
  ],
  "data": null
}
```

## License

MIT License

## Contact

Currently looking for Front End Developer position in Sydney.
If you have any feedback or job opportunities, please feel free to contact me via LinkedIn / Email!

Kevin Yen - [@Kevin_linkedIn](https://www.linkedin.com/in/kerwinyen83/) - kevinyenhaha@gmail.com