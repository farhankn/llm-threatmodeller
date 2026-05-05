# ACSE-Eval IaC source path (dataset-relative):
# aws-vdi-architecture/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_directory_service" {
  tags = {
    acse_component = "AWS Directory Service"
  }
}

resource "aws_resource" "amazon_efs" {
  tags = {
    acse_component = "Amazon EFS"
  }
}

resource "aws_resource" "amazon_fsx" {
  tags = {
    acse_component = "Amazon FSx"
  }
}

resource "aws_resource" "amazon_workspaces" {
  tags = {
    acse_component = "Amazon WorkSpaces"
  }
}

resource "aws_resource" "appstream_2_0" {
  tags = {
    acse_component = "AppStream 2.0"
  }
}

resource "aws_resource" "directory_service" {
  tags = {
    acse_component = "Directory Service"
  }
}

resource "aws_resource" "efs" {
  tags = {
    acse_component = "EFS"
  }
}

resource "aws_resource" "fsx" {
  tags = {
    acse_component = "FSx"
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

resource "aws_resource" "management_network_interface" {
  tags = {
    acse_component = "Management Network Interface"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
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

resource "aws_resource" "workspaces" {
  tags = {
    acse_component = "WorkSpaces"
  }
}
