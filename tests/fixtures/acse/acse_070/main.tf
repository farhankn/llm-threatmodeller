# ACSE-Eval IaC source path (dataset-relative):
# realtime-personalization/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_lambda_function" "api_handler_lambda" {
  tags = {
    acse_component = "API Handler Lambda"
  }
}

resource "aws_resource" "amazon_personalize" {
  tags = {
    acse_component = "Amazon Personalize"
  }
}

resource "aws_lambda_function" "analytics_lambda" {
  tags = {
    acse_component = "Analytics Lambda"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_db_instance" "dynamodb_user_profiles_table" {
  tags = {
    acse_component = "DynamoDB User Profiles Table"
  }
}

resource "aws_resource" "ecs_service" {
  tags = {
    acse_component = "ECS Service"
  }
}

resource "aws_resource" "elasticache" {
  tags = {
    acse_component = "ElastiCache"
  }
}

resource "aws_resource" "elasticache_redis" {
  tags = {
    acse_component = "ElastiCache Redis"
  }
}

resource "aws_lambda_function" "event_processor_lambda" {
  tags = {
    acse_component = "Event Processor Lambda"
  }
}

resource "aws_resource" "kinesis_event_stream" {
  tags = {
    acse_component = "Kinesis Event Stream"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "real-time_recommendation_engine_ecs" {
  tags = {
    acse_component = "Real-time Recommendation Engine (ECS)"
  }
}

resource "aws_s3_bucket" "s3_data_lake" {
  tags = {
    acse_component = "S3 Data Lake"
  }
}

resource "aws_resource" "sqs_event_queue" {
  tags = {
    acse_component = "SQS Event Queue"
  }
}
