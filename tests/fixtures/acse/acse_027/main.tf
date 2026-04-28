# ACSE-Eval IaC source path (dataset-relative):
# document-management-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "application_code" {
  tags = {
    acse_component = "Application Code"
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

resource "aws_db_instance" "dynamodb_sessions_table" {
  tags = {
    acse_component = "DynamoDB Sessions Table"
  }
}

resource "aws_resource" "ecs_fargate_tasks" {
  tags = {
    acse_component = "ECS Fargate Tasks"
  }
}

resource "aws_resource" "ecs_tasks" {
  tags = {
    acse_component = "ECS Tasks"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kms_keys" {
  tags = {
    acse_component = "KMS Keys"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_db_instance" "rds_database" {
  tags = {
    acse_component = "RDS Database"
  }
}

resource "aws_db_instance" "rds_postgresql_database" {
  tags = {
    acse_component = "RDS PostgreSQL Database"
  }
}

resource "aws_resource" "redis_cache" {
  tags = {
    acse_component = "Redis Cache"
  }
}

resource "aws_s3_bucket" "s3_archive_bucket" {
  tags = {
    acse_component = "S3 Archive Bucket"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_s3_bucket" "s3_document_bucket" {
  tags = {
    acse_component = "S3 Document Bucket"
  }
}

resource "aws_resource" "sqs_queue" {
  tags = {
    acse_component = "SQS Queue"
  }
}

resource "aws_ecr_repository" "secrets_manager" {
  tags = {
    acse_component = "Secrets Manager"
  }
}
