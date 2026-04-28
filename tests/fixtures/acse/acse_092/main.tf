# ACSE-Eval IaC source path (dataset-relative):
# temporary-access-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_iam_role" "brokerrole" {
  tags = {
    acse_component = "BrokerRole"
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

resource "aws_resource" "directoryservice" {
  tags = {
    acse_component = "DirectoryService"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_lambda_function" "lambda_authorizer" {
  tags = {
    acse_component = "Lambda Authorizer"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "sts" {
  tags = {
    acse_component = "STS"
  }
}

resource "aws_iam_role" "targetrole" {
  tags = {
    acse_component = "TargetRole"
  }
}
