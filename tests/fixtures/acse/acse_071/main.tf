# ACSE-Eval IaC source path (dataset-relative):
# recommendation-engine/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_endpoints" {
  tags = {
    acse_component = "API Endpoints"
  }
}

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "API Gateway"
  }
}

resource "aws_resource" "all_aws_services" {
  tags = {
    acse_component = "All AWS Services"
  }
}

resource "aws_resource" "client_applications" {
  tags = {
    acse_component = "Client Applications"
  }
}

resource "aws_resource" "data_flows_between_all_components" {
  tags = {
    acse_component = "Data flows between all components"
  }
}

resource "aws_resource" "ecs_service" {
  tags = {
    acse_component = "ECS Service"
  }
}

resource "aws_resource" "ecs_services" {
  tags = {
    acse_component = "ECS Services"
  }
}

resource "aws_resource" "elasticache" {
  tags = {
    acse_component = "ElastiCache"
  }
}

resource "aws_iam_role" "iam_roles" {
  tags = {
    acse_component = "IAM Roles"
  }
}

resource "aws_lambda_function" "lambda_functions" {
  tags = {
    acse_component = "Lambda Functions"
  }
}

resource "aws_resource" "load_balancer" {
  tags = {
    acse_component = "Load Balancer"
  }
}

resource "aws_lambda_function" "ml_inference_lambda" {
  tags = {
    acse_component = "ML Inference Lambda"
  }
}

resource "aws_resource" "model_loading_process" {
  tags = {
    acse_component = "Model Loading Process"
  }
}

resource "aws_db_instance" "rds_database" {
  tags = {
    acse_component = "RDS Database"
  }
}

resource "aws_s3_bucket" "s3_ml_models_bucket" {
  tags = {
    acse_component = "S3 ML Models Bucket"
  }
}

resource "aws_resource" "sagemaker_training_jobs" {
  tags = {
    acse_component = "SageMaker Training Jobs"
  }
}

resource "aws_security_group" "security_groups" {
  tags = {
    acse_component = "Security Groups"
  }
}

resource "aws_vpc" "subnets" {
  tags = {
    acse_component = "Subnets"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}
