# ACSE-Eval IaC source path (dataset-relative):
# security-insights-on-aws/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "athena_results" {
  tags = {
    acse_component = "Athena Results"
  }
}

resource "aws_resource" "cloudtrail" {
  tags = {
    acse_component = "CloudTrail"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "cloudwatch_logs" {
  tags = {
    acse_component = "CloudWatch Logs"
  }
}

resource "aws_resource" "data_sources" {
  tags = {
    acse_component = "Data Sources"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "lake_formation" {
  tags = {
    acse_component = "Lake Formation"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "opensearch_domain" {
  tags = {
    acse_component = "OpenSearch Domain"
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

resource "aws_resource" "ssm_parameter_store" {
  tags = {
    acse_component = "SSM Parameter Store"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_resource" "security_hub" {
  tags = {
    acse_component = "Security Hub"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}

resource "aws_vpc" "vpc_flow_logs" {
  tags = {
    acse_component = "VPC Flow Logs"
  }
}
