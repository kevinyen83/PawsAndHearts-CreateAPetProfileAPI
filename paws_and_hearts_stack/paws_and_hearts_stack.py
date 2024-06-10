import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class PawsAndHeartsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket_name = "pet-profile-image-bucket"
        dynamodb_table_name = "pet-table"

        s3_bucket = s3.Bucket(self, 
            "PetProfileImageBucket",
            bucket_name=s3_bucket_name,
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.PUT, s3.HttpMethods.POST, s3.HttpMethods.DELETE, s3.HttpMethods.HEAD],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                    max_age=3000
                )
            ],
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            )
        )

        s3_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"arn:aws:s3:::{s3_bucket_name}/*"]
            )
        )

        lambda_function = _lambda.Function(self, 
            "PetApiFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="app.lambda_handler",
            code=_lambda.Code.from_asset("pet_python_api"),
            environment={
                "S3_BUCKET": s3_bucket_name,
                "DYNAMODB_TABLE": dynamodb_table_name
            },
            memory_size=128,
            timeout=cdk.Duration.seconds(10)
        )

        s3_bucket.grant_read_write(lambda_function)

        api = apigateway.RestApi(self, "paws-and-hearts-pet-api",
            rest_api_name="paws-and-hearts-pet-api",
            description="API for Pet Management",
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": ["OPTIONS", "GET", "POST", "PATCH", "DELETE"],
                "allow_headers": ["Content-Type", "X-Api-Key"]
            }
        )

        request_template = {
            "application/json": """
            {
                "body" : $input.json('$')
            }
            """
        }

        integration_responses = [{
            "statusCode": "200",
            "responseTemplates": {
                "application/json": """
                #set($inputRoot = $input.path('$'))
                {
                    "statusCode": 200,
                    "message": "$inputRoot.message"
                }
                """
            },
            "responseParameters": {
                "method.response.header.Access-Control-Allow-Headers": "'Content-Type,X-Api-Key'",
                "method.response.header.Access-Control-Allow-Methods": "'OPTIONS,GET,POST,PATCH,DELETE'",
                "method.response.header.Access-Control-Allow-Origin": "'*'"
            }
        }]

        lambda_integration = apigateway.LambdaIntegration(
            lambda_function,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        health_api = api.root.add_resource("health")
        health_api.add_method("GET", lambda_integration)

        pet_api = api.root.add_resource("pet")
        pet_api.add_method("GET", lambda_integration, method_responses=[
            {
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Access-Control-Allow-Headers": True,
                    "method.response.header.Access-Control-Allow-Methods": True,
                    "method.response.header.Access-Control-Allow-Origin": True
                }
            }
        ])
        pet_api.add_method("POST", lambda_integration, request_parameters={
            "method.request.header.Content-Type": True,
            "method.request.header.X-Api-Key": True
        }, method_responses=[
            {
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Access-Control-Allow-Headers": True,
                    "method.response.header.Access-Control-Allow-Methods": True,
                    "method.response.header.Access-Control-Allow-Origin": True
                }
            }
        ])

        pet_api.add_method("DELETE", lambda_integration, method_responses=[
            {
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Access-Control-Allow-Headers": True,
                    "method.response.header.Access-Control-Allow-Methods": True,
                    "method.response.header.Access-Control-Allow-Origin": True
                }
            }
        ])

        pets_api = api.root.add_resource("pets")
        pets_api.add_method("GET", lambda_integration)

        update_api = api.root.add_resource("updateAvailability")
        update_api.add_method("PATCH", lambda_integration)

        table = dynamodb.Table(self, dynamodb_table_name,
            table_name=dynamodb_table_name,
            partition_key={"name": "petId", "type": dynamodb.AttributeType.STRING},
            removal_policy=cdk.RemovalPolicy.RETAIN
        )

        table.grant_full_access(lambda_function)

        cdk.CfnOutput(self, "PetApiEndpoint",
            value=api.url,
            description="API Gateway endpoint URL"
        )

app = cdk.App()
PawsAndHeartsStack(app, "PawsAndHeartsStack")
app.synth()