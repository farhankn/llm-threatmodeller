# ACSE-Eval IaC source path (dataset-relative):
# cryptocurrency/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "apigateway" {
  tags = {
    acse_component = "APIGateway"
  }
}

resource "aws_resource" "all_components" {
  tags = {
    acse_component = "All Components"
  }
}

resource "aws_resource" "blockchainnetwork" {
  tags = {
    acse_component = "BlockchainNetwork"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "ecs" {
  tags = {
    acse_component = "ECS"
  }
}

resource "aws_resource" "kms" {
  tags = {
    acse_component = "KMS"
  }
}

resource "aws_resource" "keystore" {
  tags = {
    acse_component = "KeyStore"
  }
}

resource "aws_lambda_function" "lambda" {
  tags = {
    acse_component = "Lambda"
  }
}

resource "aws_db_instance" "managedblockchain" {
  tags = {
    acse_component = "ManagedBlockchain"
  }
}

resource "aws_resource" "miningnodes" {
  tags = {
    acse_component = "MiningNodes"
  }
}

resource "aws_ecr_repository" "secretsmanager" {
  tags = {
    acse_component = "SecretsManager"
  }
}

resource "aws_resource" "transactionprocessors" {
  tags = {
    acse_component = "TransactionProcessors"
  }
}

resource "aws_db_instance" "walletdb" {
  tags = {
    acse_component = "WalletDB"
  }
}

resource "aws_resource" "walletservice" {
  tags = {
    acse_component = "WalletService"
  }
}
