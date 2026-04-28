# ACSE-Eval IaC source path (dataset-relative):
# rtb-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "apigateway" {
  tags = {
    acse_component = "APIGateway"
  }
}

resource "aws_resource" "adservice" {
  tags = {
    acse_component = "AdService"
  }
}

resource "aws_resource" "biddingservice" {
  tags = {
    acse_component = "BiddingService"
  }
}

resource "aws_lambda_function" "campaignmgmtlambda" {
  tags = {
    acse_component = "CampaignMgmtLambda"
  }
}

resource "aws_cloudfront_distribution" "cloudfront" {
  tags = {
    acse_component = "CloudFront"
  }
}

resource "aws_iam_role" "iam" {
  tags = {
    acse_component = "IAM"
  }
}

resource "aws_db_instance" "loadbalancer" {
  tags = {
    acse_component = "LoadBalancer"
  }
}

resource "aws_wafv2_web_acl" "waf" {
  tags = {
    acse_component = "WAF"
  }
}

resource "aws_resource" "analytics" {
  tags = {
    acse_component = "analytics"
  }
}

resource "aws_resource" "analytics_cluster" {
  tags = {
    acse_component = "analytics_cluster"
  }
}

resource "aws_resource" "bid_cache" {
  tags = {
    acse_component = "bid_cache"
  }
}

resource "aws_resource" "bid_handlers" {
  tags = {
    acse_component = "bid_handlers"
  }
}

resource "aws_resource" "bid_processors" {
  tags = {
    acse_component = "bid_processors"
  }
}

resource "aws_resource" "bid_store" {
  tags = {
    acse_component = "bid_store"
  }
}

resource "aws_db_instance" "campaign_db" {
  tags = {
    acse_component = "campaign_db"
  }
}

resource "aws_resource" "data_lake" {
  tags = {
    acse_component = "data_lake"
  }
}

resource "aws_resource" "event_stream" {
  tags = {
    acse_component = "event_stream"
  }
}
