# ACSE-Eval IaC source path (dataset-relative):
# distributed-load-testing/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "codebuild" {
  tags = {
    acse_component = "CodeBuild"
  }
}

resource "aws_resource" "codebuild_project" {
  tags = {
    acse_component = "CodeBuild Project"
  }
}

resource "aws_db_instance" "dynamodb_test_config_table" {
  tags = {
    acse_component = "DynamoDB Test Config Table"
  }
}

resource "aws_ecr_repository" "ecr_repository" {
  tags = {
    acse_component = "ECR Repository"
  }
}

resource "aws_resource" "ecs" {
  tags = {
    acse_component = "ECS"
  }
}

resource "aws_resource" "fargate_tasks" {
  tags = {
    acse_component = "Fargate Tasks"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_lambda_function" "lambda_orchestrator" {
  tags = {
    acse_component = "Lambda Orchestrator"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}
