# ACSE-Eval IaC source path (dataset-relative):
# serverless-data-pipeline/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_s3_bucket" "archivebucket" {
  tags = {
    acse_component = "ArchiveBucket"
  }
}

resource "aws_lambda_function" "dataingestionlambda" {
  tags = {
    acse_component = "DataIngestionLambda"
  }
}

resource "aws_lambda_function" "dataprocessinglambda" {
  tags = {
    acse_component = "DataProcessingLambda"
  }
}

resource "aws_lambda_function" "datatransformlambda" {
  tags = {
    acse_component = "DataTransformLambda"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_resource" "kinesis" {
  tags = {
    acse_component = "Kinesis"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_s3_bucket" "processeddatabucket" {
  tags = {
    acse_component = "ProcessedDataBucket"
  }
}

resource "aws_s3_bucket" "rawdatabucket" {
  tags = {
    acse_component = "RawDataBucket"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
  }
}
