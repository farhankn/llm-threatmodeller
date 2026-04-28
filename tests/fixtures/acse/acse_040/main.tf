# ACSE-Eval IaC source path (dataset-relative):
# human-data-collection-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_api_gateway_rest_api" "api_gateway_authorizer" {
  tags = {
    acse_component = "API Gateway Authorizer"
  }
}

resource "aws_resource" "all_aws_services" {
  tags = {
    acse_component = "All AWS Services"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "cognito_user_pool" {
  tags = {
    acse_component = "Cognito User Pool"
  }
}

resource "aws_s3_bucket" "datalake_s3_bucket" {
  tags = {
    acse_component = "DataLake S3 Bucket"
  }
}

resource "aws_resource" "ml_model" {
  tags = {
    acse_component = "ML Model"
  }
}

resource "aws_db_instance" "responses_db" {
  tags = {
    acse_component = "Responses DB"
  }
}

resource "aws_lambda_function" "task_handler_lambda" {
  tags = {
    acse_component = "Task Handler Lambda"
  }
}

resource "aws_resource" "task_queue" {
  tags = {
    acse_component = "Task Queue"
  }
}

resource "aws_db_instance" "tasks_db" {
  tags = {
    acse_component = "Tasks DB"
  }
}

resource "aws_s3_bucket" "aws-s3-datalake" {
  tags = {
    acse_component = "aws-s3-datalake"
  }
}
