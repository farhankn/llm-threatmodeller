# ACSE-Eval IaC source path (dataset-relative):
# automated-security-response/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "adminaccount" {
  tags = {
    acse_component = "AdminAccount"
  }
}

resource "aws_lambda_function" "checkstatelambda" {
  tags = {
    acse_component = "CheckStateLambda"
  }
}

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

resource "aws_lambda_function" "executeremediationlambda" {
  tags = {
    acse_component = "ExecuteRemediationLambda"
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

resource "aws_lambda_function" "lambdafunctions" {
  tags = {
    acse_component = "LambdaFunctions"
  }
}

resource "aws_resource" "memberaccount" {
  tags = {
    acse_component = "MemberAccount"
  }
}

resource "aws_s3_bucket" "metricsbucket" {
  tags = {
    acse_component = "MetricsBucket"
  }
}

resource "aws_iam_role" "remediationrole" {
  tags = {
    acse_component = "RemediationRole"
  }
}

resource "aws_resource" "sns" {
  tags = {
    acse_component = "SNS"
  }
}

resource "aws_resource" "securityhub" {
  tags = {
    acse_component = "SecurityHub"
  }
}

resource "aws_lambda_function" "sendnotificationlambda" {
  tags = {
    acse_component = "SendNotificationLambda"
  }
}

resource "aws_resource" "stepfunctions" {
  tags = {
    acse_component = "StepFunctions"
  }
}

resource "aws_resource" "systemsmanager" {
  tags = {
    acse_component = "SystemsManager"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}
