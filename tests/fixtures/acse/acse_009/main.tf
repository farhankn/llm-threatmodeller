# ACSE-Eval IaC source path (dataset-relative):
# budgeting-application/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "alb" {
  tags = {
    acse_component = "ALB"
  }
}

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "budget_analyzer" {
  tags = {
    acse_component = "Budget Analyzer"
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

resource "aws_resource" "ecs" {
  tags = {
    acse_component = "ECS"
  }
}

resource "aws_resource" "emr" {
  tags = {
    acse_component = "EMR"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_resource" "mobile_app" {
  tags = {
    acse_component = "Mobile App"
  }
}

resource "aws_resource" "notification_queue" {
  tags = {
    acse_component = "Notification Queue"
  }
}

resource "aws_db_instance" "rds" {
  tags = {
    acse_component = "RDS"
  }
}

resource "aws_resource" "redshift" {
  tags = {
    acse_component = "Redshift"
  }
}

resource "aws_resource" "sqs" {
  tags = {
    acse_component = "SQS"
  }
}

resource "aws_resource" "transaction_processor" {
  tags = {
    acse_component = "Transaction Processor"
  }
}

resource "aws_resource" "transaction_queue" {
  tags = {
    acse_component = "Transaction Queue"
  }
}

resource "aws_resource" "web_app" {
  tags = {
    acse_component = "Web App"
  }
}
