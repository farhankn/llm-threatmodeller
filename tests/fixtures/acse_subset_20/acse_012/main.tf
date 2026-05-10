# ACSE-Eval IaC source path (dataset-relative):
# code-execution-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_s3_bucket" "code_storage_s3_bucket" {
  tags = {
    acse_component = "Code Storage S3 Bucket"
  }
}

resource "aws_resource" "ecs_fargate_cluster" {
  tags = {
    acse_component = "ECS Fargate Cluster"
  }
}

resource "aws_resource" "execution_node_1" {
  tags = {
    acse_component = "Execution Node 1"
  }
}

resource "aws_resource" "execution_node_2" {
  tags = {
    acse_component = "Execution Node 2"
  }
}

resource "aws_resource" "execution_node_3" {
  tags = {
    acse_component = "Execution Node 3"
  }
}

resource "aws_lambda_function" "execution_orchestrator_lambda" {
  tags = {
    acse_component = "Execution Orchestrator Lambda"
  }
}

resource "aws_lambda_function" "result_processor_lambda" {
  tags = {
    acse_component = "Result Processor Lambda"
  }
}

resource "aws_db_instance" "results_db_dynamodb" {
  tags = {
    acse_component = "Results DB (DynamoDB)"
  }
}

resource "aws_s3_bucket" "results_storage_s3_bucket" {
  tags = {
    acse_component = "Results Storage S3 Bucket"
  }
}

resource "aws_resource" "shield" {
  tags = {
    acse_component = "Shield"
  }
}

resource "aws_wafv2_web_acl" "waf" {
  tags = {
    acse_component = "WAF"
  }
}
