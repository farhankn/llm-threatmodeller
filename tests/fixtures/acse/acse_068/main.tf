# ACSE-Eval IaC source path (dataset-relative):
# real-time-collaborative-editing/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "apigateway_websocket_api" {
  tags = {
    acse_component = "APIGateway WebSocket API"
  }
}

resource "aws_api_gateway_rest_api" "appsync_graphql_api" {
  tags = {
    acse_component = "AppSync GraphQL API"
  }
}

resource "aws_s3_bucket" "attachmentsbucket" {
  tags = {
    acse_component = "AttachmentsBucket"
  }
}

resource "aws_resource" "conflictqueue" {
  tags = {
    acse_component = "ConflictQueue"
  }
}

resource "aws_resource" "conflictresolutionhandler" {
  tags = {
    acse_component = "ConflictResolutionHandler"
  }
}

resource "aws_resource" "documentstable" {
  tags = {
    acse_component = "DocumentsTable"
  }
}

resource "aws_resource" "elasticache" {
  tags = {
    acse_component = "ElastiCache"
  }
}

resource "aws_lambda_function" "statehandlerlambda" {
  tags = {
    acse_component = "StateHandlerLambda"
  }
}

resource "aws_lambda_function" "synchandlerlambda" {
  tags = {
    acse_component = "SyncHandlerLambda"
  }
}

resource "aws_resource" "versionstable" {
  tags = {
    acse_component = "VersionsTable"
  }
}
