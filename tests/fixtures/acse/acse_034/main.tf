# ACSE-Eval IaC source path (dataset-relative):
# fraud-detection/cdk/
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

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
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

resource "aws_s3_bucket" "datalakebucket" {
  tags = {
    acse_component = "DataLakeBucket"
  }
}

resource "aws_resource" "elasticache" {
  tags = {
    acse_component = "ElastiCache"
  }
}

resource "aws_resource" "guardduty" {
  tags = {
    acse_component = "GuardDuty"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "IAM"
  }
}

resource "aws_resource" "kinesis" {
  tags = {
    acse_component = "Kinesis"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_s3_bucket" "mlmodelsbucket" {
  tags = {
    acse_component = "MlModelsBucket"
  }
}

resource "aws_db_instance" "rds" {
  tags = {
    acse_component = "RDS"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_resource" "sagemaker" {
  tags = {
    acse_component = "SageMaker"
  }
}

resource "aws_ecr_repository" "secrets_manager" {
  tags = {
    acse_component = "Secrets Manager"
  }
}
