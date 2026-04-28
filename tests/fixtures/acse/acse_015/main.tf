# ACSE-Eval IaC source path (dataset-relative):
# containerized-microservices/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "alb" {
  tags = {
    acse_component = "ALB"
  }
}

resource "aws_resource" "all_services" {
  tags = {
    acse_component = "All Services"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_ecr_repository" "ecr" {
  tags = {
    acse_component = "ECR"
  }
}

resource "aws_resource" "ecs" {
  tags = {
    acse_component = "ECS"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "IAM"
  }
}

resource "aws_resource" "nacls" {
  tags = {
    acse_component = "NACLs"
  }
}

resource "aws_db_instance" "rds" {
  tags = {
    acse_component = "RDS"
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

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}

resource "aws_resource" "x-ray" {
  tags = {
    acse_component = "X-Ray"
  }
}

resource "aws_api_gateway_rest_api" "api-service" {
  tags = {
    acse_component = "api-service"
  }
}

resource "aws_resource" "auth-service" {
  tags = {
    acse_component = "auth-service"
  }
}

resource "aws_resource" "data-service" {
  tags = {
    acse_component = "data-service"
  }
}
