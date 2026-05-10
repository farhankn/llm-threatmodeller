# ACSE-Eval IaC source path (dataset-relative):
# distributed-graph-processing/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_endpoints" {
  tags = {
    acse_component = "API Endpoints"
  }
}

resource "aws_resource" "emr_cluster" {
  tags = {
    acse_component = "EMR Cluster"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kinesis_data_stream" {
  tags = {
    acse_component = "Kinesis Data Stream"
  }
}

resource "aws_resource" "kinesis_stream" {
  tags = {
    acse_component = "Kinesis Stream"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_lambda_function" "lambda_processors" {
  tags = {
    acse_component = "Lambda Processors"
  }
}

resource "aws_db_instance" "neptune_graph_database" {
  tags = {
    acse_component = "Neptune Graph Database"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}
