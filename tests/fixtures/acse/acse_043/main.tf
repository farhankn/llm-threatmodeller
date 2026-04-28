# ACSE-Eval IaC source path (dataset-relative):
# image-video-recognition-system/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "all_components" {
  tags = {
    acse_component = "All components"
  }
}

resource "aws_resource" "all_service_communications" {
  tags = {
    acse_component = "All service communications"
  }
}

resource "aws_resource" "custom_models" {
  tags = {
    acse_component = "Custom models"
  }
}

resource "aws_resource" "ecs_processing_service" {
  tags = {
    acse_component = "ECS processing service"
  }
}

resource "aws_resource" "ecs_services" {
  tags = {
    acse_component = "ECS services"
  }
}

resource "aws_resource" "elasticache" {
  tags = {
    acse_component = "ElastiCache"
  }
}

resource "aws_resource" "elasticache_endpoints" {
  tags = {
    acse_component = "ElastiCache endpoints"
  }
}

resource "aws_iam_role" "iam_roles_and_policies" {
  tags = {
    acse_component = "IAM roles and policies"
  }
}

resource "aws_resource" "inference_endpoints" {
  tags = {
    acse_component = "Inference endpoints"
  }
}

resource "aws_resource" "kinesis_streams" {
  tags = {
    acse_component = "Kinesis streams"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda functions"
  }
}

resource "aws_lambda_function" "lambda_processing_function" {
  tags = {
    acse_component = "Lambda processing function"
  }
}

resource "aws_resource" "rekognition" {
  tags = {
    acse_component = "Rekognition"
  }
}

resource "aws_s3_bucket" "s3" {
  tags = {
    acse_component = "S3"
  }
}

resource "aws_resource" "sqs_queues" {
  tags = {
    acse_component = "SQS queues"
  }
}

resource "aws_resource" "sagemaker_endpoints" {
  tags = {
    acse_component = "SageMaker endpoints"
  }
}

resource "aws_resource" "sagemaker_notebooks" {
  tags = {
    acse_component = "SageMaker notebooks"
  }
}

resource "aws_resource" "service_communications" {
  tags = {
    acse_component = "Service communications"
  }
}

resource "aws_resource" "training_jobs" {
  tags = {
    acse_component = "Training jobs"
  }
}

resource "aws_s3_bucket" "input-storage-bucket" {
  tags = {
    acse_component = "input-storage-bucket"
  }
}

resource "aws_s3_bucket" "raw-data-lake-bucket" {
  tags = {
    acse_component = "raw-data-lake-bucket"
  }
}
