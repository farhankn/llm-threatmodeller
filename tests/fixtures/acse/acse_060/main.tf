# ACSE-Eval IaC source path (dataset-relative):
# opensearch-migration-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "application_load_balancer" {
  tags = {
    acse_component = "Application Load Balancer"
  }
}

resource "aws_resource" "msk_cluster" {
  tags = {
    acse_component = "MSK Cluster"
  }
}

resource "aws_resource" "migration_management_console" {
  tags = {
    acse_component = "Migration Management Console"
  }
}

resource "aws_s3_bucket" "s3_snapshot_storage" {
  tags = {
    acse_component = "S3 Snapshot Storage"
  }
}

resource "aws_resource" "source_opensearch_cluster" {
  tags = {
    acse_component = "Source OpenSearch Cluster"
  }
}

resource "aws_resource" "target_opensearch_cluster" {
  tags = {
    acse_component = "Target OpenSearch Cluster"
  }
}

resource "aws_resource" "traffic_capture_proxy" {
  tags = {
    acse_component = "Traffic Capture Proxy"
  }
}

resource "aws_resource" "traffic_replayer" {
  tags = {
    acse_component = "Traffic Replayer"
  }
}
