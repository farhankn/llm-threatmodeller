# ACSE-Eval IaC source path (dataset-relative):
# contact-center-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "amazon_connect" {
  tags = {
    acse_component = "Amazon Connect"
  }
}

resource "aws_resource" "amazon_connect_chat" {
  tags = {
    acse_component = "Amazon Connect Chat"
  }
}

resource "aws_resource" "application_load_balancer" {
  tags = {
    acse_component = "Application Load Balancer"
  }
}

resource "aws_resource" "chat_ui_components" {
  tags = {
    acse_component = "Chat UI Components"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_resource" "cloudwatch_logs" {
  tags = {
    acse_component = "CloudWatch Logs"
  }
}

resource "aws_db_instance" "dynamodb_tables" {
  tags = {
    acse_component = "DynamoDB Tables"
  }
}

resource "aws_resource" "frontend_applications" {
  tags = {
    acse_component = "Frontend Applications"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_iam_role" "iam_users" {
  tags = {
    acse_component = "IAM Users"
  }
}

resource "aws_resource" "kinesis_streams" {
  tags = {
    acse_component = "Kinesis Streams"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "opensearch" {
  tags = {
    acse_component = "OpenSearch"
  }
}

resource "aws_resource" "quicksight" {
  tags = {
    acse_component = "QuickSight"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_s3_bucket" "s3_recordings_bucket" {
  tags = {
    acse_component = "S3 Recordings Bucket"
  }
}

resource "aws_resource" "saml_integration" {
  tags = {
    acse_component = "SAML Integration"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
  }
}

resource "aws_resource" "websocket_endpoints" {
  tags = {
    acse_component = "WebSocket Endpoints"
  }
}
