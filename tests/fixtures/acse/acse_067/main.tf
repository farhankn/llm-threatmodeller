# ACSE-Eval IaC source path (dataset-relative):
# quantum-computing-cluster/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "all_system_components" {
  tags = {
    acse_component = "All System Components"
  }
}

resource "aws_resource" "amazon_braket" {
  tags = {
    acse_component = "Amazon Braket"
  }
}

resource "aws_resource" "braket" {
  tags = {
    acse_component = "Braket"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_instance" "ec2_instances" {
  tags = {
    acse_component = "EC2 Instances"
  }
}

resource "aws_resource" "high_performance_compute_nodes" {
  tags = {
    acse_component = "High Performance Compute Nodes"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kms" {
  tags = {
    acse_component = "KMS"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_lambda_function" "lambda_processors" {
  tags = {
    acse_component = "Lambda Processors"
  }
}

resource "aws_resource" "nacls" {
  tags = {
    acse_component = "NACLs"
  }
}

resource "aws_resource" "network_communications" {
  tags = {
    acse_component = "Network Communications"
  }
}

resource "aws_vpc" "private_subnets" {
  tags = {
    acse_component = "Private Subnets"
  }
}

resource "aws_s3_bucket" "s3_storage" {
  tags = {
    acse_component = "S3 Storage"
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

resource "aws_resource" "timestream" {
  tags = {
    acse_component = "Timestream"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}
