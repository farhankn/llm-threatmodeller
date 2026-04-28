# ACSE-Eval IaC source path (dataset-relative):
# music-streaming-service/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_cloudfront_distribution" "cloudfront_cdn" {
  tags = {
    acse_component = "CloudFront CDN"
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

resource "aws_resource" "cognito_user_pool" {
  tags = {
    acse_component = "Cognito User Pool"
  }
}

resource "aws_db_instance" "dynamodb_user_data" {
  tags = {
    acse_component = "DynamoDB User Data"
  }
}

resource "aws_resource" "ecs_services" {
  tags = {
    acse_component = "ECS Services"
  }
}

resource "aws_resource" "elasticache_clusters" {
  tags = {
    acse_component = "ElastiCache Clusters"
  }
}

resource "aws_resource" "elastic_beanstalk" {
  tags = {
    acse_component = "Elastic Beanstalk"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "mediaconvert" {
  tags = {
    acse_component = "MediaConvert"
  }
}

resource "aws_resource" "mediastore_container" {
  tags = {
    acse_component = "MediaStore Container"
  }
}

resource "aws_resource" "mobile_apps" {
  tags = {
    acse_component = "Mobile Apps"
  }
}

resource "aws_db_instance" "rds_metadata_db" {
  tags = {
    acse_component = "RDS Metadata DB"
  }
}

resource "aws_s3_bucket" "s3_music_storage" {
  tags = {
    acse_component = "S3 Music Storage"
  }
}

resource "aws_resource" "sqs_queue" {
  tags = {
    acse_component = "SQS Queue"
  }
}

resource "aws_resource" "streaming_service" {
  tags = {
    acse_component = "Streaming Service"
  }
}
