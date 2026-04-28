# ACSE-Eval IaC source path (dataset-relative):
# pki-private-ca/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_lambda_function" "certificate_issuance_lambda" {
  tags = {
    acse_component = "Certificate Issuance Lambda"
  }
}

resource "aws_lambda_function" "certificate_renewal_lambda" {
  tags = {
    acse_component = "Certificate Renewal Lambda"
  }
}

resource "aws_lambda_function" "certificate_revocation_lambda" {
  tags = {
    acse_component = "Certificate Revocation Lambda"
  }
}

resource "aws_resource" "certificate_storage" {
  tags = {
    acse_component = "Certificate Storage"
  }
}

resource "aws_s3_bucket" "certificate_storage_bucket" {
  tags = {
    acse_component = "Certificate Storage Bucket"
  }
}

resource "aws_lambda_function" "certificate_validation_lambda" {
  tags = {
    acse_component = "Certificate Validation Lambda"
  }
}

resource "aws_resource" "eventbridge_rule" {
  tags = {
    acse_component = "EventBridge Rule"
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

resource "aws_resource" "private_certificate_authority" {
  tags = {
    acse_component = "Private Certificate Authority"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}

resource "aws_resource" "systems_manager_parameters" {
  tags = {
    acse_component = "Systems Manager Parameters"
  }
}
