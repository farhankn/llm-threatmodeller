provider "aws" {
  region = "us-east-1"
}

variable "db_password" {
  type    = string
  default = "SuperSecret123!"
}

resource "aws_s3_bucket" "logs" {
  bucket = "corp-logs-public-demo"
  acl    = "public-read"
}

resource "aws_security_group" "web" {
  name = "web-open"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "app" {
  identifier            = "app-db-prod"
  engine                = "postgres"
  publicly_accessible   = true
  allocated_storage     = 20
  skip_final_snapshot   = true
  username              = "appadmin"
  password              = var.db_password
}

resource "aws_iam_policy" "wildcard_admin" {
  name   = "wildcard-admin"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "*",
        Resource = "*"
      }
    ]
  })
}
