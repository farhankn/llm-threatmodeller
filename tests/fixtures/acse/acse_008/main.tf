# ACSE-Eval IaC source path (dataset-relative):
# bird-game/cdk/
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

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "cognito" {
  tags = {
    acse_component = "Cognito"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_resource" "elasticache" {
  tags = {
    acse_component = "ElastiCache"
  }
}

resource "aws_lambda_function" "game_logic_lambda" {
  tags = {
    acse_component = "Game Logic Lambda"
  }
}

resource "aws_resource" "kinesis_data_analytics" {
  tags = {
    acse_component = "Kinesis Data Analytics"
  }
}

resource "aws_resource" "kinesis_data_streams" {
  tags = {
    acse_component = "Kinesis Data Streams"
  }
}

resource "aws_lambda_function" "leaderboard_manager_lambda" {
  tags = {
    acse_component = "Leaderboard Manager Lambda"
  }
}

resource "aws_resource" "mobile_client" {
  tags = {
    acse_component = "Mobile Client"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_resource" "sns" {
  tags = {
    acse_component = "SNS"
  }
}

resource "aws_lambda_function" "score_processor_lambda" {
  tags = {
    acse_component = "Score Processor Lambda"
  }
}
