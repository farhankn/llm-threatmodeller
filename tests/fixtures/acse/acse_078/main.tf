# ACSE-Eval IaC source path (dataset-relative):
# serverless-anomaly-detection-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "amplify" {
  tags = {
    acse_component = "Amplify"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "Cloudwatch"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "Dynamodb"
  }
}

resource "aws_resource" "kinesis" {
  tags = {
    acse_component = "Kinesis"
  }
}

resource "aws_resource" "kinesisdatastreams" {
  tags = {
    acse_component = "KinesisDataStreams"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
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

resource "aws_resource" "sagemakermodel" {
  tags = {
    acse_component = "SagemakerModel"
  }
}

resource "aws_resource" "webui" {
  tags = {
    acse_component = "WebUI"
  }
}

resource "aws_lambda_function" "anomaly_lambda" {
  tags = {
    acse_component = "anomaly_lambda"
  }
}

resource "aws_lambda_function" "notification_lambda" {
  tags = {
    acse_component = "notification_lambda"
  }
}

resource "aws_lambda_function" "preprocessing_lambda" {
  tags = {
    acse_component = "preprocessing_lambda"
  }
}
