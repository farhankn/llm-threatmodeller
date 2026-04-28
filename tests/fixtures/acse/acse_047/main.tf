# ACSE-Eval IaC source path (dataset-relative):
# live-streaming-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_api_gateway_rest_api" "api_gateway_websocket_api" {
  tags = {
    acse_component = "API Gateway WebSocket API"
  }
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  tags = {
    acse_component = "CloudFront Distribution"
  }
}

resource "aws_db_instance" "dynamodb_chat_table" {
  tags = {
    acse_component = "DynamoDB Chat Table"
  }
}

resource "aws_resource" "elasticache_redis_cluster" {
  tags = {
    acse_component = "ElastiCache Redis Cluster"
  }
}

resource "aws_resource" "elementalmedialive" {
  tags = {
    acse_component = "ElementalMediaLive"
  }
}

resource "aws_resource" "elementalmediastore" {
  tags = {
    acse_component = "ElementalMediaStore"
  }
}

resource "aws_resource" "elementalmediastore" {
  tags = {
    acse_component = "ElementalMediastore"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_lambda_function" "lambda_chat_handler" {
  tags = {
    acse_component = "Lambda Chat Handler"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "medialive_channels" {
  tags = {
    acse_component = "MediaLive Channels"
  }
}

resource "aws_security_group" "medialive_input_security_group" {
  tags = {
    acse_component = "MediaLive Input Security Group"
  }
}

resource "aws_resource" "medialive_recording_output" {
  tags = {
    acse_component = "MediaLive Recording Output"
  }
}

resource "aws_iam_policy" "mediastore_container_policy" {
  tags = {
    acse_component = "MediaStore Container Policy"
  }
}

resource "aws_resource" "rtmp_ingestion_endpoints" {
  tags = {
    acse_component = "RTMP Ingestion Endpoints"
  }
}

resource "aws_s3_bucket" "s3_recording_bucket" {
  tags = {
    acse_component = "S3 Recording Bucket"
  }
}

resource "aws_resource" "sqs_chat_queue" {
  tags = {
    acse_component = "SQS Chat Queue"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_vpc" "vpc_configuration" {
  tags = {
    acse_component = "VPC Configuration"
  }
}
