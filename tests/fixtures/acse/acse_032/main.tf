# ACSE-Eval IaC source path (dataset-relative):
# ev-charging-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "admin_api" {
  tags = {
    acse_component = "Admin API"
  }
}

resource "aws_api_gateway_rest_api" "admin_api_api_gateway" {
  tags = {
    acse_component = "Admin API (API Gateway)"
  }
}

resource "aws_db_instance" "dynamodb_telemetry_store" {
  tags = {
    acse_component = "DynamoDB (Telemetry Store)"
  }
}

resource "aws_resource" "ev_charging_station" {
  tags = {
    acse_component = "EV Charging Station"
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

resource "aws_resource" "network_load_balancer" {
  tags = {
    acse_component = "Network Load Balancer"
  }
}

resource "aws_resource" "ocpp_handler_fargate" {
  tags = {
    acse_component = "OCPP Handler (Fargate)"
  }
}

resource "aws_route53_zone" "route53_dns" {
  tags = {
    acse_component = "Route53 DNS"
  }
}

resource "aws_s3_bucket" "s3_data_lake" {
  tags = {
    acse_component = "S3 (Data Lake)"
  }
}

resource "aws_resource" "sqs_queue" {
  tags = {
    acse_component = "SQS Queue"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
  }
}
