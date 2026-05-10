# ACSE-Eval IaC source path (dataset-relative):
# digital-twin-ecosystem/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "aws_iot_sitewise" {
  tags = {
    acse_component = "AWS IoT SiteWise"
  }
}

resource "aws_resource" "aws_iot_twinmaker" {
  tags = {
    acse_component = "AWS IoT TwinMaker"
  }
}

resource "aws_resource" "aws_robomaker" {
  tags = {
    acse_component = "AWS RoboMaker"
  }
}

resource "aws_resource" "all_core_services" {
  tags = {
    acse_component = "All Core Services"
  }
}

resource "aws_resource" "all_services" {
  tags = {
    acse_component = "All Services"
  }
}

resource "aws_resource" "analytics_application" {
  tags = {
    acse_component = "Analytics Application"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_db_instance" "grafana_dashboards" {
  tags = {
    acse_component = "Grafana Dashboards"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "kinesis_data_stream" {
  tags = {
    acse_component = "Kinesis Data Stream"
  }
}

resource "aws_resource" "regular_users_group" {
  tags = {
    acse_component = "Regular Users Group"
  }
}

resource "aws_s3_bucket" "s3_workspace_bucket" {
  tags = {
    acse_component = "S3 Workspace Bucket"
  }
}

resource "aws_resource" "sqs_queue" {
  tags = {
    acse_component = "SQS Queue"
  }
}
