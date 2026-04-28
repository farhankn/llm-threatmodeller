# ACSE-Eval IaC source path (dataset-relative):
# kanban-board-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_lambda_function" "boardmanagementlambda" {
  tags = {
    acse_component = "BoardManagementLambda"
  }
}

resource "aws_lambda_function" "cardmanagementlambda" {
  tags = {
    acse_component = "CardManagementLambda"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_resource" "cognito" {
  tags = {
    acse_component = "Cognito"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_resource" "elasticache_redis" {
  tags = {
    acse_component = "ElastiCache Redis"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "sqs_event_queue" {
  tags = {
    acse_component = "SQS Event Queue"
  }
}
