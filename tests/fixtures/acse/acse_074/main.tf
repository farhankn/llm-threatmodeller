# ACSE-Eval IaC source path (dataset-relative):
# sagemaker-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_api_gateway_rest_api" "apigateway" {
  tags = {
    acse_component = "APIGateway"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_s3_bucket" "model_artifacts_s3_bucket" {
  tags = {
    acse_component = "Model Artifacts S3 Bucket"
  }
}

resource "aws_resource" "model_registry" {
  tags = {
    acse_component = "Model Registry"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_s3_bucket" "s3buckets" {
  tags = {
    acse_component = "S3Buckets"
  }
}

resource "aws_resource" "sagemaker_model" {
  tags = {
    acse_component = "SageMaker Model"
  }
}

resource "aws_resource" "sagemaker_training_jobs" {
  tags = {
    acse_component = "SageMaker Training Jobs"
  }
}

resource "aws_resource" "sagemaker_endpoints" {
  tags = {
    acse_component = "SageMaker endpoints"
  }
}

resource "aws_s3_bucket" "training_data_s3_bucket" {
  tags = {
    acse_component = "Training Data S3 Bucket"
  }
}
