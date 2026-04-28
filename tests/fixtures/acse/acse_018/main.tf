# ACSE-Eval IaC source path (dataset-relative):
# crm-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "all_components" {
  tags = {
    acse_component = "All Components"
  }
}

resource "aws_resource" "application_load_balancer" {
  tags = {
    acse_component = "Application Load Balancer"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_resource" "cognito_user_pools" {
  tags = {
    acse_component = "Cognito User Pools"
  }
}

resource "aws_db_instance" "dynamodb_table" {
  tags = {
    acse_component = "DynamoDB Table"
  }
}

resource "aws_resource" "ecs_containers" {
  tags = {
    acse_component = "ECS Containers"
  }
}

resource "aws_resource" "glue_etl" {
  tags = {
    acse_component = "Glue ETL"
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

resource "aws_resource" "quicksight" {
  tags = {
    acse_component = "QuickSight"
  }
}

resource "aws_db_instance" "rds_instance" {
  tags = {
    acse_component = "RDS Instance"
  }
}

resource "aws_resource" "redshift" {
  tags = {
    acse_component = "Redshift"
  }
}
