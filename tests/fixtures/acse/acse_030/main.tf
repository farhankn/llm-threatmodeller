# ACSE-Eval IaC source path (dataset-relative):
# email-delivery-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws-acm" {
  tags = {
    acse_component = "aws-acm"
  }
}

resource "aws_db_instance" "aws-dynamodb-metricsstore" {
  tags = {
    acse_component = "aws-dynamodb-MetricsStore"
  }
}

resource "aws_resource" "aws-elasticbeanstalk-adminpanel" {
  tags = {
    acse_component = "aws-elasticbeanstalk-AdminPanel"
  }
}

resource "aws_lambda_function" "aws-lambda-emailprocessor" {
  tags = {
    acse_component = "aws-lambda-EmailProcessor"
  }
}

resource "aws_lambda_function" "aws-lambda-notificationmanager" {
  tags = {
    acse_component = "aws-lambda-NotificationManager"
  }
}

resource "aws_route53_zone" "aws-route53" {
  tags = {
    acse_component = "aws-route53"
  }
}

resource "aws_s3_bucket" "aws-s3-emailarchivebucket" {
  tags = {
    acse_component = "aws-s3-EmailArchiveBucket"
  }
}

resource "aws_resource" "aws-ses" {
  tags = {
    acse_component = "aws-ses"
  }
}

resource "aws_resource" "aws-sqs-emailqueue" {
  tags = {
    acse_component = "aws-sqs-EmailQueue"
  }
}
