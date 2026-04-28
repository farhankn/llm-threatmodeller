# ACSE-Eval IaC source path (dataset-relative):
# multi-region-active-active-db/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_config" {
  tags = {
    acse_component = "AWS Config"
  }
}

resource "aws_resource" "aws_shield" {
  tags = {
    acse_component = "AWS Shield"
  }
}

resource "aws_resource" "application_load_balancers" {
  tags = {
    acse_component = "Application Load Balancers"
  }
}

resource "aws_db_instance" "aurora_databases" {
  tags = {
    acse_component = "Aurora Databases"
  }
}

resource "aws_db_instance" "aurora_global_database" {
  tags = {
    acse_component = "Aurora Global Database"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "cross-region_replication" {
  tags = {
    acse_component = "Cross-Region Replication"
  }
}

resource "aws_resource" "cross-region_replication_links" {
  tags = {
    acse_component = "Cross-Region Replication Links"
  }
}

resource "aws_lambda_function" "custom_merge_logic_lambda" {
  tags = {
    acse_component = "Custom Merge Logic Lambda"
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

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kms_keys" {
  tags = {
    acse_component = "KMS Keys"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_route53_zone" "route_53" {
  tags = {
    acse_component = "Route 53"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_vpc" "vpc_cross-region_communication" {
  tags = {
    acse_component = "VPC Cross-Region Communication"
  }
}

resource "aws_security_group" "vpc_lambda_security_group" {
  tags = {
    acse_component = "VPC Lambda Security Group"
  }
}

resource "aws_vpc" "vpc_peering" {
  tags = {
    acse_component = "VPC Peering"
  }
}
