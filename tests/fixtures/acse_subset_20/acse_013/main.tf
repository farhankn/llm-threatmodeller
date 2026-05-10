# ACSE-Eval IaC source path (dataset-relative):
# connected-vehicle-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "amplify_frontend" {
  tags = {
    acse_component = "Amplify Frontend"
  }
}

resource "aws_resource" "connected_vehicle" {
  tags = {
    acse_component = "Connected Vehicle"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_resource" "ecs_cluster" {
  tags = {
    acse_component = "ECS Cluster"
  }
}

resource "aws_resource" "iot_core" {
  tags = {
    acse_component = "IoT Core"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "mobile_app" {
  tags = {
    acse_component = "Mobile App"
  }
}

resource "aws_resource" "private_ca" {
  tags = {
    acse_component = "Private CA"
  }
}

resource "aws_lambda_function" "registration_lambda" {
  tags = {
    acse_component = "Registration Lambda"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}
