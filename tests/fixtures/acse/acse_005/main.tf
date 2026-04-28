# ACSE-Eval IaC source path (dataset-relative):
# big-data-processing-and-analytics-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "all_platform_components" {
  tags = {
    acse_component = "All Platform Components"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kinesis_data_analytics" {
  tags = {
    acse_component = "Kinesis Data Analytics"
  }
}

resource "aws_resource" "kinesis_data_streams" {
  tags = {
    acse_component = "Kinesis Data Streams"
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

resource "aws_resource" "msk" {
  tags = {
    acse_component = "MSK"
  }
}

resource "aws_resource" "opensearch" {
  tags = {
    acse_component = "OpenSearch"
  }
}

resource "aws_resource" "quicksight" {
  tags = {
    acse_component = "QuickSight"
  }
}

resource "aws_resource" "redshift" {
  tags = {
    acse_component = "Redshift"
  }
}

resource "aws_s3_bucket" "s3_data_lake" {
  tags = {
    acse_component = "S3 Data Lake"
  }
}

resource "aws_resource" "sagemaker" {
  tags = {
    acse_component = "SageMaker"
  }
}

resource "aws_resource" "sagemaker_endpoints" {
  tags = {
    acse_component = "SageMaker Endpoints"
  }
}
