# ACSE-Eval IaC source path (dataset-relative):
# version-control/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_db_instance" "dynamodb_global_tables" {
  tags = {
    acse_component = "DynamoDB Global Tables"
  }
}

resource "aws_db_instance" "dynamodb_repository_metadata_table" {
  tags = {
    acse_component = "DynamoDB Repository Metadata Table"
  }
}

resource "aws_resource" "elasticache_redis_cluster" {
  tags = {
    acse_component = "ElastiCache Redis Cluster"
  }
}

resource "aws_resource" "git_workers" {
  tags = {
    acse_component = "Git Workers"
  }
}

resource "aws_resource" "git_workers_ecs_tasks" {
  tags = {
    acse_component = "Git Workers (ECS Tasks)"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "IAM"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "multiple_aws_regions" {
  tags = {
    acse_component = "Multiple AWS Regions"
  }
}

resource "aws_resource" "repository_service" {
  tags = {
    acse_component = "Repository Service"
  }
}

resource "aws_s3_bucket" "s3_cross-region_replication" {
  tags = {
    acse_component = "S3 Cross-Region Replication"
  }
}

resource "aws_s3_bucket" "s3_large_object_store" {
  tags = {
    acse_component = "S3 Large Object Store"
  }
}

resource "aws_s3_bucket" "s3_repository_store" {
  tags = {
    acse_component = "S3 Repository Store"
  }
}

resource "aws_wafv2_web_acl" "waf" {
  tags = {
    acse_component = "WAF"
  }
}
