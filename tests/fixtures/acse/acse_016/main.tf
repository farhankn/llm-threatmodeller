# ACSE-Eval IaC source path (dataset-relative):
# content-localization/cdk/
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

resource "aws_lambda_function" "analytics_lambda" {
  tags = {
    acse_component = "Analytics Lambda"
  }
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  tags = {
    acse_component = "CloudFront Distribution"
  }
}

resource "aws_resource" "cloudwatch_logs" {
  tags = {
    acse_component = "CloudWatch Logs"
  }
}

resource "aws_resource" "cognito_userpool" {
  tags = {
    acse_component = "Cognito UserPool"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kinesis_stream" {
  tags = {
    acse_component = "Kinesis Stream"
  }
}

resource "aws_resource" "opensearch_domain" {
  tags = {
    acse_component = "OpenSearch Domain"
  }
}

resource "aws_lambda_function" "operator_lambda" {
  tags = {
    acse_component = "Operator Lambda"
  }
}

resource "aws_s3_bucket" "s3_dataplane_bucket" {
  tags = {
    acse_component = "S3 Dataplane Bucket"
  }
}

resource "aws_resource" "sqs_queue" {
  tags = {
    acse_component = "SQS Queue"
  }
}

resource "aws_s3_bucket" "source_media_bucket" {
  tags = {
    acse_component = "Source Media Bucket"
  }
}

resource "aws_lambda_function" "workflow_processor_lambda" {
  tags = {
    acse_component = "Workflow Processor Lambda"
  }
}
