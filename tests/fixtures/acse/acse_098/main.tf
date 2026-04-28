# ACSE-Eval IaC source path (dataset-relative):
# voice-processing-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "ai_ml_services" {
  tags = {
    acse_component = "AI/ML Services"
  }
}

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

resource "aws_db_instance" "dynamodb_table" {
  tags = {
    acse_component = "DynamoDB Table"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kms_key" {
  tags = {
    acse_component = "KMS Key"
  }
}

resource "aws_resource" "kinesis_data_streams" {
  tags = {
    acse_component = "Kinesis Data Streams"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "lex" {
  tags = {
    acse_component = "Lex"
  }
}

resource "aws_resource" "polly" {
  tags = {
    acse_component = "Polly"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_resource" "transcribe" {
  tags = {
    acse_component = "Transcribe"
  }
}
