# ACSE-Eval IaC source path (dataset-relative):
# game-analytics-pipeline/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "athena" {
  tags = {
    acse_component = "Athena"
  }
}

resource "aws_resource" "cognito_user_pool" {
  tags = {
    acse_component = "Cognito User Pool"
  }
}

resource "aws_db_instance" "dynamodb_table" {
  tags = {
    acse_component = "DynamoDB Table"
  }
}

resource "aws_resource" "emr_cluster" {
  tags = {
    acse_component = "EMR Cluster"
  }
}

resource "aws_instance" "emr_instance_profile" {
  tags = {
    acse_component = "EMR Instance Profile"
  }
}

resource "aws_iam_role" "emr_service_role" {
  tags = {
    acse_component = "EMR Service Role"
  }
}

resource "aws_resource" "game_state_data" {
  tags = {
    acse_component = "Game State Data"
  }
}

resource "aws_resource" "kinesis_data_analytics" {
  tags = {
    acse_component = "Kinesis Data Analytics"
  }
}

resource "aws_resource" "kinesis_data_firehose" {
  tags = {
    acse_component = "Kinesis Data Firehose"
  }
}

resource "aws_resource" "kinesis_data_stream" {
  tags = {
    acse_component = "Kinesis Data Stream"
  }
}

resource "aws_resource" "kinesis_data_streams" {
  tags = {
    acse_component = "Kinesis Data Streams"
  }
}

resource "aws_resource" "kinesis_firehose" {
  tags = {
    acse_component = "Kinesis Firehose"
  }
}

resource "aws_s3_bucket" "processed_data_bucket" {
  tags = {
    acse_component = "Processed Data Bucket"
  }
}

resource "aws_s3_bucket" "processed_data_s3_bucket" {
  tags = {
    acse_component = "Processed Data S3 Bucket"
  }
}

resource "aws_lambda_function" "processing_lambda" {
  tags = {
    acse_component = "Processing Lambda"
  }
}

resource "aws_resource" "quicksight" {
  tags = {
    acse_component = "QuickSight"
  }
}

resource "aws_s3_bucket" "raw_data_s3_bucket" {
  tags = {
    acse_component = "Raw Data S3 Bucket"
  }
}
