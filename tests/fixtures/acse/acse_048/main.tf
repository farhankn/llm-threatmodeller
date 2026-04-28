# ACSE-Eval IaC source path (dataset-relative):
# log-analysis-monitoring-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "firehose" {
  tags = {
    acse_component = "firehose"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "iam"
  }
}

resource "aws_resource" "kinesis_agent" {
  tags = {
    acse_component = "kinesis_agent"
  }
}

resource "aws_resource" "kinesis_analytics" {
  tags = {
    acse_component = "kinesis_analytics"
  }
}

resource "aws_resource" "kinesis_streams" {
  tags = {
    acse_component = "kinesis_streams"
  }
}

resource "aws_lambda_function" "lambda_processor" {
  tags = {
    acse_component = "lambda_processor"
  }
}

resource "aws_resource" "opensearch" {
  tags = {
    acse_component = "opensearch"
  }
}

resource "aws_s3_bucket" "s3_processed" {
  tags = {
    acse_component = "s3_processed"
  }
}

resource "aws_s3_bucket" "s3_raw" {
  tags = {
    acse_component = "s3_raw"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "security_groups"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "vpc"
  }
}
