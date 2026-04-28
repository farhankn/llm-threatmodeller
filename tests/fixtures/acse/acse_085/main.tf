# ACSE-Eval IaC source path (dataset-relative):
# service-quotas-monitor/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_lambda_function" "all_lambda_functions" {
  tags = {
    acse_component = "All Lambda Functions"
  }
}

resource "aws_resource" "cloudwatch_events" {
  tags = {
    acse_component = "CloudWatch Events"
  }
}

resource "aws_lambda_function" "cloudwatch_poller_lambda" {
  tags = {
    acse_component = "CloudWatch Poller Lambda"
  }
}

resource "aws_db_instance" "dynamodb_tables" {
  tags = {
    acse_component = "DynamoDB Tables"
  }
}

resource "aws_resource" "eventbridge" {
  tags = {
    acse_component = "EventBridge"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_db_instance" "lambda_functions_with_dynamodb_access" {
  tags = {
    acse_component = "Lambda Functions with DynamoDB access"
  }
}

resource "aws_resource" "quota_table" {
  tags = {
    acse_component = "Quota Table"
  }
}

resource "aws_resource" "sns_topic" {
  tags = {
    acse_component = "SNS Topic"
  }
}

resource "aws_resource" "sqs_queue" {
  tags = {
    acse_component = "SQS Queue"
  }
}

resource "aws_resource" "service_table" {
  tags = {
    acse_component = "Service Table"
  }
}

resource "aws_lambda_function" "slack_notifier_lambda" {
  tags = {
    acse_component = "Slack Notifier Lambda"
  }
}

resource "aws_resource" "slack_workspace" {
  tags = {
    acse_component = "Slack Workspace"
  }
}
