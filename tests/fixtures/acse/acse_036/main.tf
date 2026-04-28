# ACSE-Eval IaC source path (dataset-relative):
# gaming-screenshot-processor/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "apigateway" {
  tags = {
    acse_component = "APIGateway"
  }
}

resource "aws_lambda_function" "all_lambda_functions" {
  tags = {
    acse_component = "All Lambda functions"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_resource" "customdomain" {
  tags = {
    acse_component = "CustomDomain"
  }
}

resource "aws_resource" "dax" {
  tags = {
    acse_component = "DAX"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_lambda_function" "imageprocessorlambda" {
  tags = {
    acse_component = "ImageProcessorLambda"
  }
}

resource "aws_lambda_function" "imageretrievallambda" {
  tags = {
    acse_component = "ImageRetrievalLambda"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda functions"
  }
}

resource "aws_resource" "originaccessidentity" {
  tags = {
    acse_component = "OriginAccessIdentity"
  }
}

resource "aws_s3_bucket" "processedimagesbucket" {
  tags = {
    acse_component = "ProcessedImagesBucket"
  }
}

resource "aws_s3_bucket" "rawimagesbucket" {
  tags = {
    acse_component = "RawImagesBucket"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_lambda_function" "uploadprocessorlambda" {
  tags = {
    acse_component = "UploadProcessorLambda"
  }
}
