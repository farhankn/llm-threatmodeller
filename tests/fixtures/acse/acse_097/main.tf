# ACSE-Eval IaC source path (dataset-relative):
# virtual-waiting-room/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

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

resource "aws_lambda_function" "countermanagementlambda" {
  tags = {
    acse_component = "CounterManagementLambda"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_api_gateway_rest_api" "privateapi" {
  tags = {
    acse_component = "PrivateApi"
  }
}

resource "aws_lambda_function" "queuemanagementlambda" {
  tags = {
    acse_component = "QueueManagementLambda"
  }
}

resource "aws_resource" "redis" {
  tags = {
    acse_component = "Redis"
  }
}

resource "aws_ecr_repository" "secretsmanager" {
  tags = {
    acse_component = "SecretsManager"
  }
}

resource "aws_lambda_function" "sessionmanagementlambda" {
  tags = {
    acse_component = "SessionManagementLambda"
  }
}

resource "aws_lambda_function" "tokengenerationlambda" {
  tags = {
    acse_component = "TokenGenerationLambda"
  }
}
