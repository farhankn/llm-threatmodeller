# ACSE-Eval IaC source path (dataset-relative):
# sandboxed-game-emulators/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "application_load_balancer" {
  tags = {
    acse_component = "Application Load Balancer"
  }
}

resource "aws_resource" "auto_scaling_group" {
  tags = {
    acse_component = "Auto Scaling Group"
  }
}

resource "aws_instance" "ec2_emulator_instances" {
  tags = {
    acse_component = "EC2 Emulator Instances"
  }
}

resource "aws_resource" "efs_file_system" {
  tags = {
    acse_component = "EFS File System"
  }
}

resource "aws_resource" "elasticache_redis_cluster" {
  tags = {
    acse_component = "ElastiCache Redis Cluster"
  }
}

resource "aws_iam_role" "iam_role" {
  tags = {
    acse_component = "IAM Role"
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

resource "aws_resource" "nat_gateway" {
  tags = {
    acse_component = "NAT Gateway"
  }
}

resource "aws_vpc" "public_subnet" {
  tags = {
    acse_component = "Public Subnet"
  }
}

resource "aws_resource" "shield" {
  tags = {
    acse_component = "Shield"
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
