# ACSE-Eval IaC source path (dataset-relative):
# renewable-energy-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_endpoints" {
  tags = {
    acse_component = "API Endpoints"
  }
}

resource "aws_resource" "all_aws_services" {
  tags = {
    acse_component = "All AWS Services"
  }
}

resource "aws_resource" "all_data_transfer_paths" {
  tags = {
    acse_component = "All Data Transfer Paths"
  }
}

resource "aws_resource" "all_services" {
  tags = {
    acse_component = "All Services"
  }
}

resource "aws_resource" "athena" {
  tags = {
    acse_component = "Athena"
  }
}

resource "aws_resource" "data_flow_paths" {
  tags = {
    acse_component = "Data Flow Paths"
  }
}

resource "aws_resource" "glue_catalog" {
  tags = {
    acse_component = "Glue Catalog"
  }
}

resource "aws_resource" "glue_etl" {
  tags = {
    acse_component = "Glue ETL"
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

resource "aws_resource" "lake_formation" {
  tags = {
    acse_component = "Lake Formation"
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

resource "aws_resource" "redshift" {
  tags = {
    acse_component = "Redshift"
  }
}

resource "aws_s3_bucket" "s3_buckets" {
  tags = {
    acse_component = "S3 Buckets"
  }
}

resource "aws_s3_bucket" "s3_processed_data" {
  tags = {
    acse_component = "S3 Processed Data"
  }
}

resource "aws_s3_bucket" "s3_raw_data" {
  tags = {
    acse_component = "S3 Raw Data"
  }
}

resource "aws_resource" "sagemaker" {
  tags = {
    acse_component = "SageMaker"
  }
}

resource "aws_resource" "service_communications" {
  tags = {
    acse_component = "Service Communications"
  }
}

resource "aws_resource" "timestream" {
  tags = {
    acse_component = "Timestream"
  }
}
