# ACSE-Eval IaC source path (dataset-relative):
# ml-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_gateway" {
  tags = {
    acse_component = "api_gateway"
  }
}

resource "aws_lambda_function" "batchinferencelambda" {
  tags = {
    acse_component = "batchInferenceLambda"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "cloudwatch"
  }
}

resource "aws_resource" "cognito" {
  tags = {
    acse_component = "cognito"
  }
}

resource "aws_resource" "ecs" {
  tags = {
    acse_component = "ecs"
  }
}

resource "aws_resource" "ecstaskdefinition" {
  tags = {
    acse_component = "ecsTaskDefinition"
  }
}

resource "aws_iam_role" "ecstaskrole" {
  tags = {
    acse_component = "ecsTaskRole"
  }
}

resource "aws_resource" "event_bridge" {
  tags = {
    acse_component = "event_bridge"
  }
}

resource "aws_resource" "glue_jobs" {
  tags = {
    acse_component = "glue_jobs"
  }
}

resource "aws_lambda_function" "lambda_fn" {
  tags = {
    acse_component = "lambda_fn"
  }
}

resource "aws_s3_bucket" "modelartifactsbucket" {
  tags = {
    acse_component = "modelArtifactsBucket"
  }
}

resource "aws_s3_bucket" "processeddatabucket" {
  tags = {
    acse_component = "processedDataBucket"
  }
}

resource "aws_resource" "processed_data" {
  tags = {
    acse_component = "processed_data"
  }
}

resource "aws_resource" "raw_data" {
  tags = {
    acse_component = "raw_data"
  }
}

resource "aws_iam_role" "sagemakerexecutionrole" {
  tags = {
    acse_component = "sagemakerExecutionRole"
  }
}

resource "aws_resource" "training" {
  tags = {
    acse_component = "training"
  }
}

resource "aws_resource" "userpool" {
  tags = {
    acse_component = "userPool"
  }
}

resource "aws_resource" "userpoolclient" {
  tags = {
    acse_component = "userPoolClient"
  }
}
