provider "aws" {
  region = "eu-west-1"
}

module "network" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "demo-vpc"
  cidr   = "10.0.0.0/16"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.bastion.id]
}

resource "aws_security_group" "bastion" {
  name = "bastion-open"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "artifacts" {
  bucket = "artifacts-no-encryption-demo"
  acl    = "private"
}
