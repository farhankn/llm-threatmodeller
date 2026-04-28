# ACSE-Eval IaC source path (dataset-relative):
# sports-betting-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway_websocket" {
  tags = {
    acse_component = "API Gateway WebSocket"
  }
}

resource "aws_resource" "aurora" {
  tags = {
    acse_component = "Aurora"
  }
}

resource "aws_resource" "aurora_cluster" {
  tags = {
    acse_component = "Aurora Cluster"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_eks_cluster" "eks_cluster" {
  tags = {
    acse_component = "EKS Cluster"
  }
}

resource "aws_eks_cluster" "eks_control_plane" {
  tags = {
    acse_component = "EKS Control Plane"
  }
}

resource "aws_eks_cluster" "eks_node_groups" {
  tags = {
    acse_component = "EKS Node Groups"
  }
}

resource "aws_resource" "load_balancer" {
  tags = {
    acse_component = "Load Balancer"
  }
}

resource "aws_resource" "msk" {
  tags = {
    acse_component = "MSK"
  }
}

resource "aws_resource" "msk_cluster" {
  tags = {
    acse_component = "MSK Cluster"
  }
}

resource "aws_resource" "nat_gateway" {
  tags = {
    acse_component = "NAT Gateway"
  }
}

resource "aws_db_instance" "rds" {
  tags = {
    acse_component = "RDS"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}

resource "aws_wafv2_web_acl" "waf" {
  tags = {
    acse_component = "WAF"
  }
}
