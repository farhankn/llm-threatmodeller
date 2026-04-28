# ACSE-Eval IaC source path (dataset-relative):
# qa-chatbot/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "amazon_bedrock" {
  tags = {
    acse_component = "Amazon Bedrock"
  }
}

resource "aws_resource" "amazon_comprehend" {
  tags = {
    acse_component = "Amazon Comprehend"
  }
}

resource "aws_resource" "amazon_translate" {
  tags = {
    acse_component = "Amazon Translate"
  }
}

resource "aws_lambda_function" "bot_fulfillment_lambda" {
  tags = {
    acse_component = "Bot Fulfillment Lambda"
  }
}

resource "aws_resource" "client_applications" {
  tags = {
    acse_component = "Client Applications"
  }
}

resource "aws_resource" "cloudwatch_logs" {
  tags = {
    acse_component = "CloudWatch Logs"
  }
}

resource "aws_lambda_function" "content_designer_lambda" {
  tags = {
    acse_component = "Content Designer Lambda"
  }
}

resource "aws_db_instance" "dynamodb_configuration_table" {
  tags = {
    acse_component = "DynamoDB Configuration Table"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "opensearch_domain" {
  tags = {
    acse_component = "OpenSearch Domain"
  }
}

resource "aws_s3_bucket" "s3_content_designer_ui_bucket" {
  tags = {
    acse_component = "S3 Content Designer UI Bucket"
  }
}

resource "aws_resource" "sagemaker_llms" {
  tags = {
    acse_component = "SageMaker LLMs"
  }
}

resource "aws_api_gateway_rest_api" "websocket_api" {
  tags = {
    acse_component = "WebSocket API"
  }
}

resource "aws_api_gateway_rest_api" "websocket_api_gateway" {
  tags = {
    acse_component = "WebSocket API Gateway"
  }
}
