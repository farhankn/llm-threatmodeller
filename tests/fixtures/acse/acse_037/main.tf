# ACSE-Eval IaC source path (dataset-relative):
# healthcare-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "all_data_transmission_paths" {
  tags = {
    acse_component = "All data transmission paths"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "cloudwatch_logs" {
  tags = {
    acse_component = "CloudWatch Logs"
  }
}

resource "aws_resource" "comprehend" {
  tags = {
    acse_component = "Comprehend"
  }
}

resource "aws_db_instance" "dynamodb_table" {
  tags = {
    acse_component = "DynamoDB Table"
  }
}

resource "aws_db_instance" "dynamodb-metadatatable" {
  tags = {
    acse_component = "DynamoDB-MetadataTable"
  }
}

resource "aws_resource" "elb" {
  tags = {
    acse_component = "ELB"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_iam_role" "generallambdarole" {
  tags = {
    acse_component = "GeneralLambdaRole"
  }
}

resource "aws_resource" "healthlake" {
  tags = {
    acse_component = "HealthLake"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_lambda_function" "lambda-syntacticprocessing" {
  tags = {
    acse_component = "Lambda-SyntacticProcessing"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}

resource "aws_s3_bucket" "s3-databucket" {
  tags = {
    acse_component = "S3-DataBucket"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}

resource "aws_vpc" "vpc_flow_logs" {
  tags = {
    acse_component = "VPC Flow Logs"
  }
}

resource "aws_resource" "vpn_connection" {
  tags = {
    acse_component = "VPN Connection"
  }
}
