# ACSE-Eval IaC source path (dataset-relative):
# distributed-storage/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "all_system_components" {
  tags = {
    acse_component = "All System Components"
  }
}

resource "aws_resource" "client_communications" {
  tags = {
    acse_component = "Client Communications"
  }
}

resource "aws_db_instance" "dynamodb_metadata_store" {
  tags = {
    acse_component = "DynamoDB Metadata Store"
  }
}

resource "aws_lambda_function" "file_metadata_manager_lambda" {
  tags = {
    acse_component = "File Metadata Manager Lambda"
  }
}

resource "aws_lambda_function" "file_upload_download_handler_lambda" {
  tags = {
    acse_component = "File Upload/Download Handler Lambda"
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

resource "aws_s3_bucket" "s3_backup_storage_bucket" {
  tags = {
    acse_component = "S3 Backup Storage Bucket"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_s3_bucket" "s3_primary_storage_bucket" {
  tags = {
    acse_component = "S3 Primary Storage Bucket"
  }
}
