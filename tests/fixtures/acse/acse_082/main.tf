# ACSE-Eval IaC source path (dataset-relative):
# serverless-event-driven-architecture/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "apigateway" {
  tags = {
    acse_component = "APIGateway"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_resource" "kinesisdatastreams" {
  tags = {
    acse_component = "KinesisDataStreams"
  }
}

resource "aws_resource" "kinesisfirehose" {
  tags = {
    acse_component = "KinesisFirehose"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_resource" "sns" {
  tags = {
    acse_component = "SNS"
  }
}

resource "aws_resource" "sqs" {
  tags = {
    acse_component = "SQS"
  }
}

resource "aws_resource" "stepfunctions" {
  tags = {
    acse_component = "StepFunctions"
  }
}
