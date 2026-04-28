# ACSE-Eval IaC source path (dataset-relative):
# serverless-cicd/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_ecr_repository" "buildsecrets" {
  tags = {
    acse_component = "BuildSecrets"
  }
}

resource "aws_resource" "cloudformation" {
  tags = {
    acse_component = "CloudFormation"
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

resource "aws_resource" "codebuild" {
  tags = {
    acse_component = "CodeBuild"
  }
}

resource "aws_resource" "codepipeline" {
  tags = {
    acse_component = "CodePipeline"
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

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "pipeline_environment_variables" {
  tags = {
    acse_component = "Pipeline Environment Variables"
  }
}

resource "aws_resource" "pipeline_metrics" {
  tags = {
    acse_component = "Pipeline Metrics"
  }
}

resource "aws_s3_bucket" "s3_artifacts" {
  tags = {
    acse_component = "S3 Artifacts"
  }
}

resource "aws_resource" "sns_alerts" {
  tags = {
    acse_component = "SNS Alerts"
  }
}

resource "aws_ecr_repository" "secretsmanager" {
  tags = {
    acse_component = "SecretsManager"
  }
}

resource "aws_resource" "source_repository" {
  tags = {
    acse_component = "Source Repository"
  }
}

resource "aws_resource" "npm_dependencies" {
  tags = {
    acse_component = "npm dependencies"
  }
}
