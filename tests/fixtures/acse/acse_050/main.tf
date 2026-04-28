# ACSE-Eval IaC source path (dataset-relative):
# ml-training-platform/cdk/
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

resource "aws_resource" "cloudtrail" {
  tags = {
    acse_component = "CloudTrail"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_lambda_function" "data_validation_lambda" {
  tags = {
    acse_component = "Data Validation Lambda"
  }
}

resource "aws_resource" "efs_file_system" {
  tags = {
    acse_component = "EFS File System"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_lambda_function" "lambda_function" {
  tags = {
    acse_component = "Lambda Function"
  }
}

resource "aws_s3_bucket" "model_artifacts_s3_bucket" {
  tags = {
    acse_component = "Model Artifacts S3 Bucket"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_resource" "sagemaker_training_jobs" {
  tags = {
    acse_component = "SageMaker Training Jobs"
  }
}

resource "aws_resource" "training_data_flow" {
  tags = {
    acse_component = "Training Data Flow"
  }
}

resource "aws_s3_bucket" "training_data_s3_bucket" {
  tags = {
    acse_component = "Training Data S3 Bucket"
  }
}
