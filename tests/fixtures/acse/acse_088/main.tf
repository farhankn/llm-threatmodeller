# ACSE-Eval IaC source path (dataset-relative):
# sovereign-cloud-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_outposts" {
  tags = {
    acse_component = "AWS Outposts"
  }
}

resource "aws_resource" "cloudhsm" {
  tags = {
    acse_component = "CloudHSM"
  }
}

resource "aws_resource" "data_residency_controls" {
  tags = {
    acse_component = "Data Residency Controls"
  }
}

resource "aws_resource" "direct_connect" {
  tags = {
    acse_component = "Direct Connect"
  }
}

resource "aws_resource" "local_compute" {
  tags = {
    acse_component = "Local Compute"
  }
}

resource "aws_resource" "local_data_center" {
  tags = {
    acse_component = "Local Data Center"
  }
}

resource "aws_resource" "local_storage" {
  tags = {
    acse_component = "Local Storage"
  }
}

resource "aws_vpc" "local_vpc" {
  tags = {
    acse_component = "Local VPC"
  }
}

resource "aws_resource" "nitro_enclaves" {
  tags = {
    acse_component = "Nitro Enclaves"
  }
}

resource "aws_resource" "private_networking" {
  tags = {
    acse_component = "Private Networking"
  }
}

resource "aws_s3_bucket" "s3_data_storage" {
  tags = {
    acse_component = "S3 (Data Storage)"
  }
}

resource "aws_ecr_repository" "secrets_manager" {
  tags = {
    acse_component = "Secrets Manager"
  }
}

resource "aws_resource" "transit_gateway" {
  tags = {
    acse_component = "Transit Gateway"
  }
}
