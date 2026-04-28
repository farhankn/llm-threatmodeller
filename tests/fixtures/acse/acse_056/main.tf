# ACSE-Eval IaC source path (dataset-relative):
# multi-region-hyperpod/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "datasync" {
  tags = {
    acse_component = "DataSync"
  }
}

resource "aws_instance" "ec2_nodes" {
  tags = {
    acse_component = "EC2 Nodes"
  }
}

resource "aws_resource" "efs_storage" {
  tags = {
    acse_component = "EFS Storage"
  }
}

resource "aws_resource" "efs_storage_both_regions" {
  tags = {
    acse_component = "EFS Storage (both regions)"
  }
}

resource "aws_eks_cluster" "eks_clusters" {
  tags = {
    acse_component = "EKS Clusters"
  }
}

resource "aws_vpc" "vpc_us-east-1" {
  tags = {
    acse_component = "VPC (us-east-1)"
  }
}

resource "aws_vpc" "vpc_us-west-2" {
  tags = {
    acse_component = "VPC (us-west-2)"
  }
}
