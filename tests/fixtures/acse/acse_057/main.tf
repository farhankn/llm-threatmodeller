# ACSE-Eval IaC source path (dataset-relative):
# multiplayer-game-server/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "auto_scaling_group" {
  tags = {
    acse_component = "Auto Scaling Group"
  }
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  tags = {
    acse_component = "CloudFront Distribution"
  }
}

resource "aws_resource" "cloudwatch_alarms" {
  tags = {
    acse_component = "CloudWatch Alarms"
  }
}

resource "aws_db_instance" "dynamodb_table" {
  tags = {
    acse_component = "DynamoDB Table"
  }
}

resource "aws_instance" "ec2_game_servers" {
  tags = {
    acse_component = "EC2 Game Servers"
  }
}

resource "aws_resource" "elasticache_cluster" {
  tags = {
    acse_component = "ElastiCache Cluster"
  }
}

resource "aws_lambda_function" "game_logic_lambda" {
  tags = {
    acse_component = "Game Logic Lambda"
  }
}

resource "aws_resource" "game_state_cache" {
  tags = {
    acse_component = "Game State Cache"
  }
}

resource "aws_api_gateway_rest_api" "rest_api_gateway" {
  tags = {
    acse_component = "REST API Gateway"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_security_group" "vpc_security_groups" {
  tags = {
    acse_component = "VPC Security Groups"
  }
}

resource "aws_api_gateway_rest_api" "websocket_api_gateway" {
  tags = {
    acse_component = "WebSocket API Gateway"
  }
}
