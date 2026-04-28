# ACSE-Eval IaC source path (dataset-relative):
# efs-filesystem/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  tags = {
    acse_component = "CloudFront Distribution"
  }
}

resource "aws_resource" "cognito_identity_pool" {
  tags = {
    acse_component = "Cognito Identity Pool"
  }
}

resource "aws_resource" "cognito_user_pool" {
  tags = {
    acse_component = "Cognito User Pool"
  }
}

resource "aws_resource" "efs_access_point" {
  tags = {
    acse_component = "EFS Access Point"
  }
}

resource "aws_resource" "efs_file_system" {
  tags = {
    acse_component = "EFS File System"
  }
}

resource "aws_resource" "efs_mount_targets" {
  tags = {
    acse_component = "EFS Mount Targets"
  }
}

resource "aws_lambda_function" "lambda_api_handler" {
  tags = {
    acse_component = "Lambda API Handler"
  }
}

resource "aws_lambda_function" "lambda_file_manager" {
  tags = {
    acse_component = "Lambda File Manager"
  }
}

resource "aws_lambda_function" "lambda_file_manager_function" {
  tags = {
    acse_component = "Lambda File Manager Function"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}
