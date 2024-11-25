from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_lambda,
    aws_apigateway as apigateway
)
from constructs import Construct

class AssignmentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Add DynamoDB table with task_id as partition key and subtask_id as sort key
        table = dynamodb.Table(
            self, "TasksTable",
            table_name="tasks",
            partition_key=dynamodb.Attribute(
                name="task_id", 
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="subtask_id", 
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,            
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )        
        
        # Add lambda function get_all_items and add environment variables
        # Add lambda function to get all items from DynamoDB table
        get_all_items = aws_lambda.Function(
            self, "GetAllItemsFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler", 
            code=aws_lambda.Code.from_asset("assignment/lambdas/get_all_items"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name
            }
        )

        # Grant read permissions to the lambda function
        table.grant_read_data(get_all_items)        

        # Add an api gateway
        api = apigateway.RestApi(
            self, "TasksApi",
            rest_api_name="Tasks API",
            description="API for managing tasks"
        )

        # Create tasks resource and GET method
        tasks = api.root.add_resource("task")
        tasks.add_method(
            "GET",
            apigateway.LambdaIntegration(get_all_items)
        )
        
