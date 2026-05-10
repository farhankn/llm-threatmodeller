# ACSE-Eval IaC source path (dataset-relative):
# biological-compute-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_batch" {
  tags = {
    acse_component = "AWS Batch"
  }
}

resource "aws_resource" "cognito_identity_pool" {
  tags = {
    acse_component = "Cognito Identity Pool"
  }
}

resource "aws_resource" "cognito_user_pool" {
  tags = {
    acse_component = "Cognito User Pool"
  }
}

resource "aws_db_instance" "dynamodb_tables" {
  tags = {
    acse_component = "DynamoDB Tables"
  }
}

resource "aws_instance" "ec2_instances" {
  tags = {
    acse_component = "EC2 Instances"
  }
}

resource "aws_resource" "efs" {
  tags = {
    acse_component = "EFS"
  }
}

resource "aws_resource" "efs_filesystem" {
  tags = {
    acse_component = "EFS FileSystem"
  }
}

resource "aws_resource" "efs_storage" {
  tags = {
    acse_component = "EFS Storage"
  }
}

resource "aws_resource" "fsx_lustre" {
  tags = {
    acse_component = "FSx Lustre"
  }
}

resource "aws_resource" "hpc_cluster" {
  tags = {
    acse_component = "HPC Cluster"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kms_key" {
  tags = {
    acse_component = "KMS Key"
  }
}

resource "aws_resource" "network_communications" {
  tags = {
    acse_component = "Network Communications"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}

resource "aws_s3_bucket" "s3_primary_data_bucket" {
  tags = {
    acse_component = "S3 Primary Data Bucket"
  }
}

resource "aws_resource" "sagemaker" {
  tags = {
    acse_component = "SageMaker"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_resource" "shared_cpu_resources" {
  tags = {
    acse_component = "Shared CPU Resources"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
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
