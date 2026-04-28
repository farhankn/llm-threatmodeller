# ACSE-Eval IaC source path (dataset-relative):
# enhanced-document-understanding/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  tags = {
    acse_component = "CloudFront Distribution"
  }
}

resource "aws_lambda_function" "generate_presigned_url_lambda" {
  tags = {
    acse_component = "Generate Presigned URL Lambda"
  }
}

resource "aws_resource" "kendra_index" {
  tags = {
    acse_component = "Kendra Index"
  }
}

resource "aws_s3_bucket" "s3_raw_documents_bucket" {
  tags = {
    acse_component = "S3 Raw Documents Bucket"
  }
}

resource "aws_lambda_function" "search_lambda" {
  tags = {
    acse_component = "Search Lambda"
  }
}

resource "aws_resource" "step_functions_workflows" {
  tags = {
    acse_component = "Step Functions Workflows"
  }
}

resource "aws_lambda_function" "task_lambdas" {
  tags = {
    acse_component = "Task Lambdas"
  }
}

resource "aws_lambda_function" "workflow_orchestrator_lambda" {
  tags = {
    acse_component = "Workflow Orchestrator Lambda"
  }
}
