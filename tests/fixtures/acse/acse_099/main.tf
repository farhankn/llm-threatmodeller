# ACSE-Eval IaC source path (dataset-relative):
# weather-forecasting-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "apigateway" {
  tags = {
    acse_component = "APIGateway"
  }
}

resource "aws_lambda_function" "apigetforecastlambda" {
  tags = {
    acse_component = "ApiGetForecastLambda"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_resource" "dataprocessor" {
  tags = {
    acse_component = "DataProcessor"
  }
}

resource "aws_resource" "elasticache" {
  tags = {
    acse_component = "ElastiCache"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_resource" "forecastcache" {
  tags = {
    acse_component = "ForecastCache"
  }
}

resource "aws_resource" "forecastgenerator" {
  tags = {
    acse_component = "ForecastGenerator"
  }
}

resource "aws_resource" "kinesisdataanalytics" {
  tags = {
    acse_component = "KinesisDataAnalytics"
  }
}

resource "aws_resource" "kinesisdatafirehose" {
  tags = {
    acse_component = "KinesisDataFirehose"
  }
}

resource "aws_resource" "kinesisfirehose" {
  tags = {
    acse_component = "KinesisFirehose"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_resource" "processeddatastorage" {
  tags = {
    acse_component = "ProcessedDataStorage"
  }
}

resource "aws_resource" "rawdataqueue" {
  tags = {
    acse_component = "RawDataQueue"
  }
}

resource "aws_resource" "rawdatastorage" {
  tags = {
    acse_component = "RawDataStorage"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_resource" "timestream" {
  tags = {
    acse_component = "Timestream"
  }
}

resource "aws_wafv2_web_acl" "waf" {
  tags = {
    acse_component = "WAF"
  }
}
