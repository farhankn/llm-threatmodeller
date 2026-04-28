# ACSE-Eval IaC source path (dataset-relative):
# serverless-etl-pipeline/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_resource" "glue" {
  tags = {
    acse_component = "Glue"
  }
}

resource "aws_resource" "glue_crawler" {
  tags = {
    acse_component = "Glue Crawler"
  }
}

resource "aws_resource" "glue_etl_jobs" {
  tags = {
    acse_component = "Glue ETL Jobs"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_resource" "mobile_device" {
  tags = {
    acse_component = "Mobile Device"
  }
}

resource "aws_s3_bucket" "processeddatabucket" {
  tags = {
    acse_component = "ProcessedDataBucket"
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

resource "aws_s3_bucket" "sourcedatabucket" {
  tags = {
    acse_component = "SourceDataBucket"
  }
}

resource "aws_resource" "stepfunctions" {
  tags = {
    acse_component = "StepFunctions"
  }
}

resource "aws_resource" "tablet_laptop" {
  tags = {
    acse_component = "Tablet/Laptop"
  }
}
