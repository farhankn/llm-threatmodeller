# ACSE-Eval IaC source path (dataset-relative):
# text-paste-service/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "aws-apigateway-textpasteapi" {
  tags = {
    acse_component = "aws-apigateway-TextPasteApi"
  }
}

resource "aws_db_instance" "aws-dynamodb-metadataddbtable" {
  tags = {
    acse_component = "aws-dynamodb-MetadataDDBTable"
  }
}

resource "aws_api_gateway_rest_api" "aws-elasticache-apicache" {
  tags = {
    acse_component = "aws-elasticache-ApiCache"
  }
}

resource "aws_lambda_function" "aws-lambda-createpastefunction" {
  tags = {
    acse_component = "aws-lambda-CreatePasteFunction"
  }
}

resource "aws_lambda_function" "aws-lambda-deletepastefunction" {
  tags = {
    acse_component = "aws-lambda-DeletePasteFunction"
  }
}

resource "aws_lambda_function" "aws-lambda-getpastefunction" {
  tags = {
    acse_component = "aws-lambda-GetPasteFunction"
  }
}

resource "aws_s3_bucket" "aws-s3-contentstorebucket" {
  tags = {
    acse_component = "aws-s3-ContentStoreBucket"
  }
}
