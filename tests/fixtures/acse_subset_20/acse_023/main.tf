# ACSE-Eval IaC source path (dataset-relative):
# distributed-cache-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_db_instance" "applicationloadbalancer" {
  tags = {
    acse_component = "ApplicationLoadBalancer"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_db_instance" "dynamodb" {
  tags = {
    acse_component = "DynamoDB"
  }
}

resource "aws_instance" "ec2-appservers" {
  tags = {
    acse_component = "EC2-AppServers"
  }
}

resource "aws_resource" "elasticache-primary" {
  tags = {
    acse_component = "ElastiCache-Primary"
  }
}

resource "aws_resource" "elasticache-secondary" {
  tags = {
    acse_component = "ElastiCache-Secondary"
  }
}

resource "aws_lambda_function" "rollbackhandlerlambda" {
  tags = {
    acse_component = "RollbackHandlerLambda"
  }
}

resource "aws_route53_zone" "route53" {
  tags = {
    acse_component = "Route53"
  }
}

resource "aws_resource" "securitygroups" {
  tags = {
    acse_component = "SecurityGroups"
  }
}

resource "aws_resource" "transitgateway" {
  tags = {
    acse_component = "TransitGateway"
  }
}
