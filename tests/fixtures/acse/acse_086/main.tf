# ACSE-Eval IaC source path (dataset-relative):
# simple-image-upload-download-website/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "application_load_balancer" {
  tags = {
    acse_component = "Application Load Balancer"
  }
}

resource "aws_resource" "application_logic" {
  tags = {
    acse_component = "Application Logic"
  }
}

resource "aws_resource" "client-server_communication" {
  tags = {
    acse_component = "Client-Server Communication"
  }
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
  tags = {
    acse_component = "CloudFront Distribution"
  }
}

resource "aws_instance" "ec2_web_server" {
  tags = {
    acse_component = "EC2 Web Server"
  }
}

resource "aws_resource" "pre-signed_url_generation_logic" {
  tags = {
    acse_component = "Pre-signed URL Generation Logic"
  }
}

resource "aws_s3_bucket" "s3_bucket" {
  tags = {
    acse_component = "S3 Bucket"
  }
}

resource "aws_s3_bucket" "s3_image_bucket" {
  tags = {
    acse_component = "S3 Image Bucket"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}
