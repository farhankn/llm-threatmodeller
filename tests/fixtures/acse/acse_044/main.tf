# ACSE-Eval IaC source path (dataset-relative):
# iot-device-management-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "certificate_manager" {
  tags = {
    acse_component = "Certificate Manager"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_db_instance" "dynamodb_device_registry_table" {
  tags = {
    acse_component = "DynamoDB Device Registry Table"
  }
}

resource "aws_db_instance" "dynamodb_tables" {
  tags = {
    acse_component = "DynamoDB Tables"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "iot_core" {
  tags = {
    acse_component = "IoT Core"
  }
}

resource "aws_resource" "iot_device_management" {
  tags = {
    acse_component = "IoT Device Management"
  }
}

resource "aws_resource" "kinesis_data_stream" {
  tags = {
    acse_component = "Kinesis Data Stream"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_lambda_function" "notification_lambda" {
  tags = {
    acse_component = "Notification Lambda"
  }
}

resource "aws_lambda_function" "processing_lambda" {
  tags = {
    acse_component = "Processing Lambda"
  }
}

resource "aws_resource" "quicksight" {
  tags = {
    acse_component = "QuickSight"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}

resource "aws_s3_bucket" "s3_bucket_longtermstoragebucket" {
  tags = {
    acse_component = "S3 Bucket (LongTermStorageBucket)"
  }
}

resource "aws_resource" "sns_alerts" {
  tags = {
    acse_component = "SNS Alerts"
  }
}

resource "aws_resource" "timestream" {
  tags = {
    acse_component = "Timestream"
  }
}

resource "aws_lambda_function" "update_lambda" {
  tags = {
    acse_component = "Update Lambda"
  }
}
