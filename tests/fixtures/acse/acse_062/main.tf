# ACSE-Eval IaC source path (dataset-relative):
# payroll-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_lambda_function" "all_lambda_functions" {
  tags = {
    acse_component = "All Lambda Functions"
  }
}

resource "aws_db_instance" "aurora_db_cluster" {
  tags = {
    acse_component = "Aurora DB Cluster"
  }
}

resource "aws_db_instance" "databases" {
  tags = {
    acse_component = "Databases"
  }
}

resource "aws_resource" "deadletterqueue" {
  tags = {
    acse_component = "DeadLetterQueue"
  }
}

resource "aws_db_instance" "dynamodb_tables" {
  tags = {
    acse_component = "DynamoDB Tables"
  }
}

resource "aws_db_instance" "dynamodb_tables_employerstatus_employeestatus" {
  tags = {
    acse_component = "DynamoDB Tables (EmployerStatus, EmployeeStatus)"
  }
}

resource "aws_resource" "external_payment_system" {
  tags = {
    acse_component = "External Payment System"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "mobile_users" {
  tags = {
    acse_component = "Mobile Users"
  }
}

resource "aws_lambda_function" "moneymovementlambda" {
  tags = {
    acse_component = "MoneyMovementLambda"
  }
}

resource "aws_resource" "processdlqqueue" {
  tags = {
    acse_component = "ProcessDlqQueue"
  }
}

resource "aws_resource" "pushpaymentqueue" {
  tags = {
    acse_component = "PushPaymentQueue"
  }
}

resource "aws_db_instance" "rds_proxy" {
  tags = {
    acse_component = "RDS Proxy"
  }
}

resource "aws_lambda_function" "redrivelambda" {
  tags = {
    acse_component = "RedriveLambda"
  }
}

resource "aws_s3_bucket" "s3_employerdatabucket_employeedatabucket" {
  tags = {
    acse_component = "S3 (EmployerDataBucket, EmployeeDataBucket)"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_resource" "sns_topic" {
  tags = {
    acse_component = "SNS Topic"
  }
}

resource "aws_resource" "shield" {
  tags = {
    acse_component = "Shield"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
  }
}

resource "aws_wafv2_web_acl" "waf" {
  tags = {
    acse_component = "WAF"
  }
}
