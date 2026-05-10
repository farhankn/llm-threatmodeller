# ACSE-Eval IaC source path (dataset-relative):
# centralized-network-inspection/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_network_firewall" {
  tags = {
    acse_component = "AWS Network Firewall"
  }
}

resource "aws_resource" "cloudwatch_logs" {
  tags = {
    acse_component = "CloudWatch Logs"
  }
}

resource "aws_resource" "codebuild" {
  tags = {
    acse_component = "CodeBuild"
  }
}

resource "aws_resource" "codepipeline" {
  tags = {
    acse_component = "CodePipeline"
  }
}

resource "aws_s3_bucket" "configbucket" {
  tags = {
    acse_component = "ConfigBucket"
  }
}

resource "aws_vpc" "firewall_subnet_1" {
  tags = {
    acse_component = "Firewall Subnet 1"
  }
}

resource "aws_vpc" "firewall_subnet_2" {
  tags = {
    acse_component = "Firewall Subnet 2"
  }
}

resource "aws_iam_role" "firewalldeployrole" {
  tags = {
    acse_component = "FirewallDeployRole"
  }
}

resource "aws_s3_bucket" "firewalllogsbucket" {
  tags = {
    acse_component = "FirewallLogsBucket"
  }
}

resource "aws_vpc" "inspection_vpc" {
  tags = {
    acse_component = "Inspection VPC"
  }
}

resource "aws_resource" "network_firewall" {
  tags = {
    acse_component = "Network Firewall"
  }
}

resource "aws_vpc" "spoke_vpcs" {
  tags = {
    acse_component = "Spoke VPCs"
  }
}

resource "aws_resource" "transit_gateway" {
  tags = {
    acse_component = "Transit Gateway"
  }
}

resource "aws_vpc" "vpc_attachments" {
  tags = {
    acse_component = "VPC Attachments"
  }
}
