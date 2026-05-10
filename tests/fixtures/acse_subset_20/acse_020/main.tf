# ACSE-Eval IaC source path (dataset-relative):
# data-viz-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  tags = {
    acse_component = "CloudFront Distribution"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_lambda_function" "dataprocessor_lambda" {
  tags = {
    acse_component = "DataProcessor Lambda"
  }
}

resource "aws_db_instance" "dynamodb_metadata_store" {
  tags = {
    acse_component = "DynamoDB Metadata Store"
  }
}

resource "aws_db_instance" "dynamodb_table" {
  tags = {
    acse_component = "DynamoDB Table"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_s3_bucket" "processed_data_bucket" {
  tags = {
    acse_component = "Processed Data Bucket"
  }
}

resource "aws_s3_bucket" "raw_data_bucket" {
  tags = {
    acse_component = "Raw Data Bucket"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_resource" "sqs_processing_queue" {
  tags = {
    acse_component = "SQS Processing Queue"
  }
}

resource "aws_s3_bucket" "staticwebsitebucket" {
  tags = {
    acse_component = "StaticWebsiteBucket"
  }
}

resource "aws_lambda_function" "uploadhandler_lambda" {
  tags = {
    acse_component = "UploadHandler Lambda"
  }
}
