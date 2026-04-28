# ACSE-Eval IaC source path (dataset-relative):
# app-runner/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_codebuild" {
  tags = {
    acse_component = "AWS CodeBuild"
  }
}

resource "aws_resource" "aws_codestar" {
  tags = {
    acse_component = "AWS CodeStar"
  }
}

resource "aws_ecr_repository" "app_runner_ecr" {
  tags = {
    acse_component = "App Runner ECR"
  }
}

resource "aws_resource" "app_runner_service" {
  tags = {
    acse_component = "App Runner Service"
  }
}

resource "aws_resource" "cloudwatch_logs" {
  tags = {
    acse_component = "CloudWatch Logs"
  }
}

resource "aws_ecr_repository" "customer_ecr" {
  tags = {
    acse_component = "Customer ECR"
  }
}

resource "aws_vpc" "customer_vpc" {
  tags = {
    acse_component = "Customer VPC"
  }
}

resource "aws_resource" "fargate_tasks" {
  tags = {
    acse_component = "Fargate Tasks"
  }
}

resource "aws_resource" "github_source_repo" {
  tags = {
    acse_component = "GitHub Source Repo"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "internet_gateway" {
  tags = {
    acse_component = "Internet Gateway"
  }
}

resource "aws_resource" "kms" {
  tags = {
    acse_component = "KMS"
  }
}

resource "aws_resource" "nat_gateway" {
  tags = {
    acse_component = "NAT Gateway"
  }
}

resource "aws_resource" "network_load_balancer" {
  tags = {
    acse_component = "Network Load Balancer"
  }
}

resource "aws_resource" "parameter_store" {
  tags = {
    acse_component = "Parameter Store"
  }
}

resource "aws_route53_zone" "route_53" {
  tags = {
    acse_component = "Route 53"
  }
}

resource "aws_ecr_repository" "secrets_manager" {
  tags = {
    acse_component = "Secrets Manager"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}
