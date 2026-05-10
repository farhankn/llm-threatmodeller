# ACSE-Eval IaC source path (dataset-relative):
# eks-outposts/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "container_network_interface_cni" {
  tags = {
    acse_component = "Container Network Interface (CNI)"
  }
}

resource "aws_resource" "customer_router" {
  tags = {
    acse_component = "Customer Router"
  }
}

resource "aws_resource" "direct_connect" {
  tags = {
    acse_component = "Direct Connect"
  }
}

resource "aws_eks_cluster" "eks_control_plane" {
  tags = {
    acse_component = "EKS Control Plane"
  }
}

resource "aws_eks_cluster" "eks_pods" {
  tags = {
    acse_component = "EKS Pods"
  }
}

resource "aws_eks_cluster" "eks_worker_nodes" {
  tags = {
    acse_component = "EKS Worker Nodes"
  }
}

resource "aws_resource" "edge_router" {
  tags = {
    acse_component = "Edge Router"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "local_gateway" {
  tags = {
    acse_component = "Local Gateway"
  }
}

resource "aws_resource" "local_gateway_lgw" {
  tags = {
    acse_component = "Local Gateway (LGW)"
  }
}

resource "aws_resource" "oidc_provider" {
  tags = {
    acse_component = "OIDC Provider"
  }
}

resource "aws_resource" "outposts_rack" {
  tags = {
    acse_component = "Outposts Rack"
  }
}

resource "aws_resource" "route_tables" {
  tags = {
    acse_component = "Route Tables"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_resource" "service_accounts" {
  tags = {
    acse_component = "Service Accounts"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}

resource "aws_vpc" "vpc_endpoints" {
  tags = {
    acse_component = "VPC Endpoints"
  }
}

resource "aws_vpc" "vpc_subnets" {
  tags = {
    acse_component = "VPC Subnets"
  }
}
