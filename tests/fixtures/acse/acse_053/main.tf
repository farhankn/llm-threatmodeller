# ACSE-Eval IaC source path (dataset-relative):
# multi-region-consensus-protocol/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_db_instance" "dynamodb_global_tables" {
  tags = {
    acse_component = "DynamoDB Global Tables"
  }
}

resource "aws_db_instance" "dynamodb_tables" {
  tags = {
    acse_component = "DynamoDB Tables"
  }
}

resource "aws_resource" "efs" {
  tags = {
    acse_component = "EFS"
  }
}

resource "aws_security_group" "efs_mount_target_security_groups" {
  tags = {
    acse_component = "EFS Mount Target Security Groups"
  }
}

resource "aws_resource" "efs_primary_us-west-2" {
  tags = {
    acse_component = "EFS Primary (us-west-2)"
  }
}

resource "aws_resource" "efs_primary_and_secondary" {
  tags = {
    acse_component = "EFS Primary and Secondary"
  }
}

resource "aws_resource" "efs_replication" {
  tags = {
    acse_component = "EFS Replication"
  }
}

resource "aws_resource" "efs_secondary_eu-west-1" {
  tags = {
    acse_component = "EFS Secondary (eu-west-1)"
  }
}

resource "aws_resource" "efs_secondary_us-east-1" {
  tags = {
    acse_component = "EFS Secondary (us-east-1)"
  }
}

resource "aws_lambda_function" "lambda_controllers" {
  tags = {
    acse_component = "Lambda Controllers"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_security_group" "lambda_security_groups" {
  tags = {
    acse_component = "Lambda Security Groups"
  }
}

resource "aws_resource" "step_functions" {
  tags = {
    acse_component = "Step Functions"
  }
}

resource "aws_resource" "transit_gateway" {
  tags = {
    acse_component = "Transit Gateway"
  }
}
