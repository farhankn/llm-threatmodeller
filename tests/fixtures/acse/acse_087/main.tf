# ACSE-Eval IaC source path (dataset-relative):
# social-media-backend/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "application_load_balancer" {
  tags = {
    acse_component = "Application Load Balancer"
  }
}

resource "aws_db_instance" "aurora_postgresql" {
  tags = {
    acse_component = "Aurora PostgreSQL"
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

resource "aws_resource" "content_service" {
  tags = {
    acse_component = "Content Service"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_resource" "ecs_services" {
  tags = {
    acse_component = "ECS Services"
  }
}

resource "aws_resource" "msk" {
  tags = {
    acse_component = "MSK"
  }
}

resource "aws_resource" "notification_service" {
  tags = {
    acse_component = "Notification Service"
  }
}

resource "aws_resource" "opensearch" {
  tags = {
    acse_component = "OpenSearch"
  }
}

resource "aws_resource" "redis" {
  tags = {
    acse_component = "Redis"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_ecr_repository" "secrets_manager" {
  tags = {
    acse_component = "Secrets Manager"
  }
}

resource "aws_resource" "social_service" {
  tags = {
    acse_component = "Social Service"
  }
}

resource "aws_resource" "user_service" {
  tags = {
    acse_component = "User Service"
  }
}
