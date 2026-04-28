# ACSE-Eval IaC source path (dataset-relative):
# unreal-engine-streaming/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "client_browser" {
  tags = {
    acse_component = "Client Browser"
  }
}

resource "aws_resource" "signaling_server" {
  tags = {
    acse_component = "Signaling Server"
  }
}

resource "aws_resource" "userdata_script" {
  tags = {
    acse_component = "UserData script"
  }
}

resource "aws_resource" "webrtc_stream" {
  tags = {
    acse_component = "WebRTC Stream"
  }
}

resource "aws_api_gateway_rest_api" "aws-api-gateway" {
  tags = {
    acse_component = "aws-api-gateway"
  }
}

resource "aws_resource" "aws-cognito-user-pool" {
  tags = {
    acse_component = "aws-cognito-user-pool"
  }
}

resource "aws_db_instance" "aws-dynamodb-instance-metadata" {
  tags = {
    acse_component = "aws-dynamodb-instance-metadata"
  }
}

resource "aws_instance" "aws-ec2-streaming-instance" {
  tags = {
    acse_component = "aws-ec2-streaming-instance"
  }
}

resource "aws_lambda_function" "aws-lambda-matchmaker" {
  tags = {
    acse_component = "aws-lambda-matchmaker"
  }
}

resource "aws_lambda_function" "aws-lambda-status-check" {
  tags = {
    acse_component = "aws-lambda-status-check"
  }
}

resource "aws_s3_bucket" "aws-s3-game-assets" {
  tags = {
    acse_component = "aws-s3-game-assets"
  }
}

resource "aws_resource" "aws-sqs-request-queue" {
  tags = {
    acse_component = "aws-sqs-request-queue"
  }
}
