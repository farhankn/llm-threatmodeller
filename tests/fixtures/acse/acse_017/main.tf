# ACSE-Eval IaC source path (dataset-relative):
# cost-management/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "apigateway" {
  tags = {
    acse_component = "APIGateway"
  }
}

resource "aws_resource" "cloudcredentials" {
  tags = {
    acse_component = "CloudCredentials"
  }
}

resource "aws_db_instance" "dynamodb-costdatabase" {
  tags = {
    acse_component = "DynamoDB-CostDatabase"
  }
}

resource "aws_resource" "eventbridge-scheduler" {
  tags = {
    acse_component = "EventBridge-Scheduler"
  }
}

resource "aws_iam_role" "iam-authentication" {
  tags = {
    acse_component = "IAM-Authentication"
  }
}

resource "aws_lambda_function" "lambda-costanalyzer" {
  tags = {
    acse_component = "Lambda-CostAnalyzer"
  }
}

resource "aws_lambda_function" "lambda-costcollector" {
  tags = {
    acse_component = "Lambda-CostCollector"
  }
}

resource "aws_lambda_function" "lambda-costprocessor" {
  tags = {
    acse_component = "Lambda-CostProcessor"
  }
}

resource "aws_s3_bucket" "s3-processeddata" {
  tags = {
    acse_component = "S3-ProcessedData"
  }
}

resource "aws_s3_bucket" "s3-rawcostdata" {
  tags = {
    acse_component = "S3-RawCostData"
  }
}

resource "aws_ecr_repository" "secretsmanager" {
  tags = {
    acse_component = "SecretsManager"
  }
}
