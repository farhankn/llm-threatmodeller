# ACSE-Eval IaC source path (dataset-relative):
# multi-region-backup-archival/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_backup" {
  tags = {
    acse_component = "AWS Backup"
  }
}

resource "aws_resource" "aurora_clusters" {
  tags = {
    acse_component = "Aurora Clusters"
  }
}

resource "aws_db_instance" "aurora_global_database" {
  tags = {
    acse_component = "Aurora Global Database"
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

resource "aws_s3_bucket" "primary_s3_bucket" {
  tags = {
    acse_component = "Primary S3 Bucket"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_s3_bucket" "s3_glacier_storage" {
  tags = {
    acse_component = "S3 Glacier Storage"
  }
}

resource "aws_s3_bucket" "s3_replication_configuration" {
  tags = {
    acse_component = "S3 Replication Configuration"
  }
}

resource "aws_s3_bucket" "secondary_s3_bucket" {
  tags = {
    acse_component = "Secondary S3 Bucket"
  }
}

resource "aws_resource" "storage_gateway" {
  tags = {
    acse_component = "Storage Gateway"
  }
}
