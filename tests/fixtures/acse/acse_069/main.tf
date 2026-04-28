# ACSE-Eval IaC source path (dataset-relative):
# realtime-analytics/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_db_instance" "dynamodb_state_table" {
  tags = {
    acse_component = "DynamoDB State Table"
  }
}

resource "aws_resource" "emr_cluster" {
  tags = {
    acse_component = "EMR Cluster"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_resource" "kinesis_analytics" {
  tags = {
    acse_component = "Kinesis Analytics"
  }
}

resource "aws_resource" "kinesis_data_streams" {
  tags = {
    acse_component = "Kinesis Data Streams"
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

resource "aws_resource" "quicksight_dashboard" {
  tags = {
    acse_component = "QuickSight Dashboard"
  }
}

resource "aws_s3_bucket" "s3_data_lake" {
  tags = {
    acse_component = "S3 Data Lake"
  }
}

resource "aws_db_instance" "timestream_database" {
  tags = {
    acse_component = "Timestream Database"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}

resource "aws_wafv2_web_acl" "waf" {
  tags = {
    acse_component = "WAF"
  }
}
