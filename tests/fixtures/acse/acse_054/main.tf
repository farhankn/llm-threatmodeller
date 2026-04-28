# ACSE-Eval IaC source path (dataset-relative):
# multi-region-dr-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_db_instance" "aurora_databases" {
  tags = {
    acse_component = "Aurora Databases"
  }
}

resource "aws_db_instance" "aurora_global_database" {
  tags = {
    acse_component = "Aurora Global Database"
  }
}

resource "aws_resource" "backup_region_alb" {
  tags = {
    acse_component = "Backup Region ALB"
  }
}

resource "aws_s3_bucket" "backup_region_s3" {
  tags = {
    acse_component = "Backup Region S3"
  }
}

resource "aws_resource" "cross-region_replication" {
  tags = {
    acse_component = "Cross-Region Replication"
  }
}

resource "aws_resource" "dr_region_alb" {
  tags = {
    acse_component = "DR Region ALB"
  }
}

resource "aws_s3_bucket" "dr_region_s3" {
  tags = {
    acse_component = "DR Region S3"
  }
}

resource "aws_db_instance" "dynamodb_global_tables" {
  tags = {
    acse_component = "DynamoDB Global Tables"
  }
}

resource "aws_db_instance" "dynamodb_tables" {
  tags = {
    acse_component = "DynamoDB Tables"
  }
}

resource "aws_instance" "ec2_instances" {
  tags = {
    acse_component = "EC2 Instances"
  }
}

resource "aws_resource" "ecs_clusters" {
  tags = {
    acse_component = "ECS Clusters"
  }
}

resource "aws_resource" "kms_keys" {
  tags = {
    acse_component = "KMS Keys"
  }
}

resource "aws_lambda_function" "lambda_environment_variables" {
  tags = {
    acse_component = "Lambda Environment Variables"
  }
}

resource "aws_lambda_function" "lambda_failover_handler" {
  tags = {
    acse_component = "Lambda Failover Handler"
  }
}

resource "aws_lambda_function" "lambda_handlers" {
  tags = {
    acse_component = "Lambda Handlers"
  }
}

resource "aws_resource" "primary_region_alb" {
  tags = {
    acse_component = "Primary Region ALB"
  }
}

resource "aws_s3_bucket" "primary_region_s3" {
  tags = {
    acse_component = "Primary Region S3"
  }
}

resource "aws_route53_zone" "route_53" {
  tags = {
    acse_component = "Route 53"
  }
}

resource "aws_route53_zone" "route_53_dns" {
  tags = {
    acse_component = "Route 53 DNS"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_s3_bucket" "s3_cross-region_replication" {
  tags = {
    acse_component = "S3 Cross-Region Replication"
  }
}
