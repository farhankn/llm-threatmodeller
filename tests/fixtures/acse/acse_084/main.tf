# ACSE-Eval IaC source path (dataset-relative):
# serverless-payment-processing-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "cloudwatch_logs" {
  tags = {
    acse_component = "CloudWatch Logs"
  }
}

resource "aws_resource" "dead_letter_queue" {
  tags = {
    acse_component = "Dead Letter Queue"
  }
}

resource "aws_db_instance" "dynamodb_backups" {
  tags = {
    acse_component = "DynamoDB Backups"
  }
}

resource "aws_db_instance" "dynamodb_transactions_table" {
  tags = {
    acse_component = "DynamoDB Transactions Table"
  }
}

resource "aws_instance" "ec2_processor" {
  tags = {
    acse_component = "EC2 Processor"
  }
}

resource "aws_lambda_function" "event_orchestrator_lambda" {
  tags = {
    acse_component = "Event Orchestrator Lambda"
  }
}

resource "aws_lambda_function" "idempotency_checker_lambda" {
  tags = {
    acse_component = "Idempotency Checker Lambda"
  }
}

resource "aws_resource" "kms_encryption_keys" {
  tags = {
    acse_component = "KMS Encryption Keys"
  }
}

resource "aws_resource" "kinesis_stream" {
  tags = {
    acse_component = "Kinesis Stream"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "main_payment_queue" {
  tags = {
    acse_component = "Main Payment Queue"
  }
}

resource "aws_lambda_function" "payment_processor_lambda" {
  tags = {
    acse_component = "Payment Processor Lambda"
  }
}

resource "aws_lambda_function" "payment_reconciliation_lambda" {
  tags = {
    acse_component = "Payment Reconciliation Lambda"
  }
}

resource "aws_db_instance" "rds_automated_backups" {
  tags = {
    acse_component = "RDS Automated Backups"
  }
}

resource "aws_db_instance" "rds_customer_database" {
  tags = {
    acse_component = "RDS Customer Database"
  }
}

resource "aws_resource" "retry_queue" {
  tags = {
    acse_component = "Retry Queue"
  }
}

resource "aws_s3_bucket" "s3_backup_bucket" {
  tags = {
    acse_component = "S3 Backup Bucket"
  }
}

resource "aws_resource" "sqs_queues" {
  tags = {
    acse_component = "SQS Queues"
  }
}
