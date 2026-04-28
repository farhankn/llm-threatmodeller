# ACSE-Eval IaC source path (dataset-relative):
# streaming-media-service/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws-alb" {
  tags = {
    acse_component = "aws-alb"
  }
}

resource "aws_resource" "aws-appsync" {
  tags = {
    acse_component = "aws-appsync"
  }
}

resource "aws_cloudfront_distribution" "aws-cloudfront" {
  tags = {
    acse_component = "aws-cloudfront"
  }
}

resource "aws_resource" "aws-cognito" {
  tags = {
    acse_component = "aws-cognito"
  }
}

resource "aws_db_instance" "aws-dynamodb" {
  tags = {
    acse_component = "aws-dynamodb"
  }
}

resource "aws_resource" "aws-elementallive" {
  tags = {
    acse_component = "aws-elementallive"
  }
}

resource "aws_resource" "aws-elementalmediaconnect" {
  tags = {
    acse_component = "aws-elementalmediaconnect"
  }
}

resource "aws_resource" "aws-elementalmediaconvert" {
  tags = {
    acse_component = "aws-elementalmediaconvert"
  }
}

resource "aws_resource" "aws-elementalmediapackage" {
  tags = {
    acse_component = "aws-elementalmediapackage"
  }
}

resource "aws_resource" "aws-elementalmediastore" {
  tags = {
    acse_component = "aws-elementalmediastore"
  }
}

resource "aws_iam_role" "aws-iam" {
  tags = {
    acse_component = "aws-iam"
  }
}

resource "aws_lambda_function" "aws-lambda" {
  tags = {
    acse_component = "aws-lambda"
  }
}

resource "aws_resource" "aws-medialive" {
  tags = {
    acse_component = "aws-medialive"
  }
}

resource "aws_resource" "aws-mediapackage" {
  tags = {
    acse_component = "aws-mediapackage"
  }
}

resource "aws_resource" "aws-mediastore" {
  tags = {
    acse_component = "aws-mediastore"
  }
}

resource "aws_db_instance" "aws-rds" {
  tags = {
    acse_component = "aws-rds"
  }
}

resource "aws_s3_bucket" "aws-s3-assets" {
  tags = {
    acse_component = "aws-s3-assets"
  }
}

resource "aws_s3_bucket" "aws-s3-media-storage" {
  tags = {
    acse_component = "aws-s3-media-storage"
  }
}

resource "aws_resource" "aws-sns" {
  tags = {
    acse_component = "aws-sns"
  }
}

resource "aws_resource" "aws-sqs" {
  tags = {
    acse_component = "aws-sqs"
  }
}

resource "aws_wafv2_web_acl" "aws-waf" {
  tags = {
    acse_component = "aws-waf"
  }
}
