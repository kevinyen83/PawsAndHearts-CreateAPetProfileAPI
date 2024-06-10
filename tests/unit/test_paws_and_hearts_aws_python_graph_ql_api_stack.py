import aws_cdk as core
import aws_cdk.assertions as assertions

from paws_and_hearts_aws_python_graph_ql_api.paws_and_hearts_aws_python_graph_ql_api_stack import PawsAndHeartsAwsPythonGraphQlApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in paws_and_hearts_aws_python_graph_ql_api/paws_and_hearts_aws_python_graph_ql_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PawsAndHeartsAwsPythonGraphQlApiStack(app, "paws-and-hearts-aws-python-graph-ql-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
