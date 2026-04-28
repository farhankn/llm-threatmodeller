# ACSE-Eval IaC source path (dataset-relative):
# iot-predictive-maintenance/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "cloudwatch_alarms" {
  tags = {
    acse_component = "CloudWatch Alarms"
  }
}

resource "aws_resource" "edge_ml_models" {
  tags = {
    acse_component = "Edge ML Models"
  }
}

resource "aws_resource" "greengrass_core" {
  tags = {
    acse_component = "Greengrass Core"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_resource" "iot_core" {
  tags = {
    acse_component = "IoT Core"
  }
}

resource "aws_resource" "iot_devices" {
  tags = {
    acse_component = "IoT Devices"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_lambda_function" "lambda_processor" {
  tags = {
    acse_component = "Lambda Processor"
  }
}

resource "aws_resource" "mqtt_protocol" {
  tags = {
    acse_component = "MQTT Protocol"
  }
}

resource "aws_resource" "quicksight" {
  tags = {
    acse_component = "QuickSight"
  }
}

resource "aws_db_instance" "quicksight_dashboards" {
  tags = {
    acse_component = "QuickSight Dashboards"
  }
}

resource "aws_resource" "sagemaker" {
  tags = {
    acse_component = "SageMaker"
  }
}

resource "aws_resource" "sagemaker_endpoint" {
  tags = {
    acse_component = "SageMaker Endpoint"
  }
}

resource "aws_resource" "sagemaker_models" {
  tags = {
    acse_component = "SageMaker Models"
  }
}

resource "aws_db_instance" "timestream_database" {
  tags = {
    acse_component = "Timestream Database"
  }
}
