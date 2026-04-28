# ACSE-Eval IaC source path (dataset-relative):
# hybrid-integration/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "customer_gateway" {
  tags = {
    acse_component = "Customer Gateway"
  }
}

resource "aws_resource" "dms" {
  tags = {
    acse_component = "DMS"
  }
}

resource "aws_resource" "direct_connect" {
  tags = {
    acse_component = "Direct Connect"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "IAM"
  }
}

resource "aws_lambda_function" "lambda_integration_service" {
  tags = {
    acse_component = "Lambda Integration Service"
  }
}

resource "aws_db_instance" "rds" {
  tags = {
    acse_component = "RDS"
  }
}

resource "aws_resource" "vpn_connection" {
  tags = {
    acse_component = "VPN Connection"
  }
}

resource "aws_resource" "virtual_private_gateway" {
  tags = {
    acse_component = "Virtual Private Gateway"
  }
}
