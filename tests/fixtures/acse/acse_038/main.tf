# ACSE-Eval IaC source path (dataset-relative):
# hpc-cluster/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "alb" {
  tags = {
    acse_component = "alb"
  }
}

resource "aws_resource" "aws-alb" {
  tags = {
    acse_component = "aws-alb"
  }
}

resource "aws_resource" "aws-efs" {
  tags = {
    acse_component = "aws-efs"
  }
}

resource "aws_s3_bucket" "aws-s3-training-data" {
  tags = {
    acse_component = "aws-s3-training-data"
  }
}

resource "aws_resource" "efs" {
  tags = {
    acse_component = "efs"
  }
}

resource "aws_resource" "https-listener" {
  tags = {
    acse_component = "https-listener"
  }
}

resource "aws_resource" "hyperpod-nodes" {
  tags = {
    acse_component = "hyperpod-nodes"
  }
}

resource "aws_iam_role" "iam-roles" {
  tags = {
    acse_component = "iam-roles"
  }
}

resource "aws_resource" "security-groups" {
  tags = {
    acse_component = "security-groups"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "vpc"
  }
}
