# ACSE-Eval IaC source path (dataset-relative):
# serverless-optimization/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "apigateway" {
  tags = {
    acse_component = "APIGateway"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_db_instance" "dynamodb-optimizationhistory" {
  tags = {
    acse_component = "DynamoDB-OptimizationHistory"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_iam_role" "iam-executorrole" {
  tags = {
    acse_component = "IAM-ExecutorRole"
  }
}

resource "aws_lambda_function" "lambda-actionexecutor" {
  tags = {
    acse_component = "Lambda-ActionExecutor"
  }
}

resource "aws_lambda_function" "lambda-all" {
  tags = {
    acse_component = "Lambda-All"
  }
}

resource "aws_lambda_function" "lambda-costanalyzer" {
  tags = {
    acse_component = "Lambda-CostAnalyzer"
  }
}

resource "aws_lambda_function" "lambda-resourceoptimizer" {
  tags = {
    acse_component = "Lambda-ResourceOptimizer"
  }
}

resource "aws_s3_bucket" "s3-costreports" {
  tags = {
    acse_component = "S3-CostReports"
  }
}

resource "aws_resource" "sns" {
  tags = {
    acse_component = "SNS"
  }
}

resource "aws_resource" "stepfunctions" {
  tags = {
    acse_component = "StepFunctions"
  }
}
