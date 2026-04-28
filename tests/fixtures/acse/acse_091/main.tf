# ACSE-Eval IaC source path (dataset-relative):
# support-ticketing-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "backend_service" {
  tags = {
    acse_component = "Backend Service"
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

resource "aws_db_instance" "dynamodb_ticket_store" {
  tags = {
    acse_component = "DynamoDB (Ticket Store)"
  }
}

resource "aws_resource" "ecs_services" {
  tags = {
    acse_component = "ECS Services"
  }
}

resource "aws_resource" "frontend_service" {
  tags = {
    acse_component = "Frontend Service"
  }
}

resource "aws_resource" "identity_center" {
  tags = {
    acse_component = "Identity Center"
  }
}

resource "aws_resource" "kms" {
  tags = {
    acse_component = "KMS"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_db_instance" "rds" {
  tags = {
    acse_component = "RDS"
  }
}

resource "aws_db_instance" "rds_user_database" {
  tags = {
    acse_component = "RDS (User Database)"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_s3_bucket" "s3_attachments" {
  tags = {
    acse_component = "S3 (Attachments)"
  }
}

resource "aws_resource" "sns_notifications" {
  tags = {
    acse_component = "SNS (Notifications)"
  }
}

resource "aws_resource" "sqs_ticket_queue" {
  tags = {
    acse_component = "SQS (Ticket Queue)"
  }
}
