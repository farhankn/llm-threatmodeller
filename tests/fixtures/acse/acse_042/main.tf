# ACSE-Eval IaC source path (dataset-relative):
# identity-management/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_organizations" {
  tags = {
    acse_component = "AWS Organizations"
  }
}

resource "aws_resource" "cloudtrail" {
  tags = {
    acse_component = "CloudTrail"
  }
}

resource "aws_resource" "corporate_identity_provider" {
  tags = {
    acse_component = "Corporate Identity Provider"
  }
}

resource "aws_db_instance" "dynamodb_audit_logs" {
  tags = {
    acse_component = "DynamoDB Audit Logs"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "IAM"
  }
}

resource "aws_iam_role" "iam_identity_center" {
  tags = {
    acse_component = "IAM Identity Center"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "member_accounts" {
  tags = {
    acse_component = "Member Accounts"
  }
}

resource "aws_resource" "network_infrastructure" {
  tags = {
    acse_component = "Network Infrastructure"
  }
}

resource "aws_resource" "public_authentication_endpoint" {
  tags = {
    acse_component = "Public Authentication Endpoint"
  }
}
