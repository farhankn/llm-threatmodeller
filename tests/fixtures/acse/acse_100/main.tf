# ACSE-Eval IaC source path (dataset-relative):
# workflow-management/cdk/
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

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "IAM"
  }
}

resource "aws_lambda_function" "lambda_task_processor" {
  tags = {
    acse_component = "Lambda Task Processor"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
  }
}
