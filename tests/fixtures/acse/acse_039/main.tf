# ACSE-Eval IaC source path (dataset-relative):
# hpc-grid-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_directory_service" {
  tags = {
    acse_component = "AWS Directory Service"
  }
}

resource "aws_resource" "aws_glue" {
  tags = {
    acse_component = "AWS Glue"
  }
}

resource "aws_resource" "athena" {
  tags = {
    acse_component = "Athena"
  }
}

resource "aws_resource" "auto_scaling_group" {
  tags = {
    acse_component = "Auto Scaling Group"
  }
}

resource "aws_instance" "ec2_compute_nodes" {
  tags = {
    acse_component = "EC2 Compute Nodes"
  }
}

resource "aws_instance" "ec2_head_nodes" {
  tags = {
    acse_component = "EC2 Head Nodes"
  }
}

resource "aws_instance" "ec2_instances" {
  tags = {
    acse_component = "EC2 Instances"
  }
}

resource "aws_resource" "fsx_for_windows" {
  tags = {
    acse_component = "FSx for Windows"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_s3_bucket" "s3_buckets_rawdatabucket_processeddatabucket" {
  tags = {
    acse_component = "S3 Buckets (RawDataBucket, ProcessedDataBucket)"
  }
}

resource "aws_resource" "sagemaker" {
  tags = {
    acse_component = "SageMaker"
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

resource "aws_resource" "storage_gateway" {
  tags = {
    acse_component = "Storage Gateway"
  }
}
