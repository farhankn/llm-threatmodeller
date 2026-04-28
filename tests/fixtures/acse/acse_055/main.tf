# ACSE-Eval IaC source path (dataset-relative):
# multi-region-eks/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "container_runtime" {
  tags = {
    acse_component = "Container Runtime"
  }
}

resource "aws_resource" "cross-region_communication" {
  tags = {
    acse_component = "Cross-Region Communication"
  }
}

resource "aws_db_instance" "dynamodb_tables" {
  tags = {
    acse_component = "DynamoDB Tables"
  }
}

resource "aws_resource" "efs_filesystem" {
  tags = {
    acse_component = "EFS FileSystem"
  }
}

resource "aws_eks_cluster" "eks_cluster" {
  tags = {
    acse_component = "EKS Cluster"
  }
}

resource "aws_eks_cluster" "eks_worker_nodes" {
  tags = {
    acse_component = "EKS Worker Nodes"
  }
}

resource "aws_iam_role" "iam_auth" {
  tags = {
    acse_component = "IAM Auth"
  }
}

resource "aws_resource" "node_groups" {
  tags = {
    acse_component = "Node Groups"
  }
}

resource "aws_resource" "persistent_storage" {
  tags = {
    acse_component = "Persistent Storage"
  }
}

resource "aws_api_gateway_rest_api" "public_apis" {
  tags = {
    acse_component = "Public APIs"
  }
}

resource "aws_resource" "state_store" {
  tags = {
    acse_component = "State Store"
  }
}

resource "aws_wafv2_web_acl" "waf" {
  tags = {
    acse_component = "WAF"
  }
}

resource "aws_resource" "worker_nodes" {
  tags = {
    acse_component = "Worker Nodes"
  }
}
