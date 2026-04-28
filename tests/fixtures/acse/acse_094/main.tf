# ACSE-Eval IaC source path (dataset-relative):
# transit-gateway/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "cognito_user_pool" {
  tags = {
    acse_component = "Cognito User Pool"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_resource" "eventbridge_rules" {
  tags = {
    acse_component = "EventBridge Rules"
  }
}

resource "aws_api_gateway_rest_api" "graphql_api" {
  tags = {
    acse_component = "GraphQL API"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_resource" "route_table" {
  tags = {
    acse_component = "Route Table"
  }
}

resource "aws_resource" "transit_gateway" {
  tags = {
    acse_component = "Transit Gateway"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}
