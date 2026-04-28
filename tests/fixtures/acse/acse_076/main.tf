# ACSE-Eval IaC source path (dataset-relative):
# search-engine/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_api_gateway_rest_api" "api_handlers" {
  tags = {
    acse_component = "API Handlers"
  }
}

resource "aws_resource" "amazon_kendra" {
  tags = {
    acse_component = "Amazon Kendra"
  }
}

resource "aws_resource" "client_applications" {
  tags = {
    acse_component = "Client Applications"
  }
}

resource "aws_resource" "elasticache_redis" {
  tags = {
    acse_component = "ElastiCache Redis"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "IAM"
  }
}

resource "aws_resource" "internal_network" {
  tags = {
    acse_component = "Internal Network"
  }
}

resource "aws_resource" "internal_services" {
  tags = {
    acse_component = "Internal Services"
  }
}

resource "aws_resource" "kendra" {
  tags = {
    acse_component = "Kendra"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_s3_bucket" "s3_document_store" {
  tags = {
    acse_component = "S3 Document Store"
  }
}

resource "aws_resource" "search_service" {
  tags = {
    acse_component = "Search Service"
  }
}
