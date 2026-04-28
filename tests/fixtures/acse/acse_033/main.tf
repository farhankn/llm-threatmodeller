# ACSE-Eval IaC source path (dataset-relative):
# flight-information-management/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "application_load_balancer" {
  tags = {
    acse_component = "Application Load Balancer"
  }
}

resource "aws_resource" "approval_service" {
  tags = {
    acse_component = "Approval Service"
  }
}

resource "aws_db_instance" "aurora_database" {
  tags = {
    acse_component = "Aurora Database"
  }
}

resource "aws_db_instance" "aurora_database_connections" {
  tags = {
    acse_component = "Aurora Database Connections"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "container_images" {
  tags = {
    acse_component = "Container Images"
  }
}

resource "aws_db_instance" "dynamodb_table" {
  tags = {
    acse_component = "DynamoDB Table"
  }
}

resource "aws_resource" "ecs_cluster" {
  tags = {
    acse_component = "ECS Cluster"
  }
}

resource "aws_resource" "ecs_services" {
  tags = {
    acse_component = "ECS Services"
  }
}

resource "aws_resource" "ecs_tasks" {
  tags = {
    acse_component = "ECS Tasks"
  }
}

resource "aws_resource" "elasticache_connections" {
  tags = {
    acse_component = "ElastiCache Connections"
  }
}

resource "aws_resource" "flight_planning_service" {
  tags = {
    acse_component = "Flight Planning Service"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
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
