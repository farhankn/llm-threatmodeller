# ACSE-Eval IaC source path (dataset-relative):
# cicd-microservices/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_api_gateway_rest_api" "api_endpoints" {
  tags = {
    acse_component = "API Endpoints"
  }
}

resource "aws_db_instance" "applicationloadbalancer" {
  tags = {
    acse_component = "ApplicationLoadBalancer"
  }
}

resource "aws_resource" "ci_cd_pipeline" {
  tags = {
    acse_component = "CI/CD Pipeline"
  }
}

resource "aws_resource" "cloudtrail" {
  tags = {
    acse_component = "CloudTrail"
  }
}

resource "aws_resource" "cloudwatch" {
  tags = {
    acse_component = "CloudWatch"
  }
}

resource "aws_resource" "codebuild" {
  tags = {
    acse_component = "CodeBuild"
  }
}

resource "aws_resource" "codebuild_project" {
  tags = {
    acse_component = "CodeBuild Project"
  }
}

resource "aws_iam_role" "codebuildrole" {
  tags = {
    acse_component = "CodeBuildRole"
  }
}

resource "aws_resource" "codecommit_repository" {
  tags = {
    acse_component = "CodeCommit Repository"
  }
}

resource "aws_resource" "codedeploy" {
  tags = {
    acse_component = "CodeDeploy"
  }
}

resource "aws_resource" "codepipeline" {
  tags = {
    acse_component = "CodePipeline"
  }
}

resource "aws_db_instance" "dynamodb_table" {
  tags = {
    acse_component = "DynamoDB Table"
  }
}

resource "aws_ecr_repository" "ecr_repositories" {
  tags = {
    acse_component = "ECR Repositories"
  }
}

resource "aws_resource" "ecs_services" {
  tags = {
    acse_component = "ECS Services"
  }
}

resource "aws_resource" "ecs_tasks" {
  tags = {
    acse_component = "ECS Tasks"
  }
}

resource "aws_iam_role" "ecstaskexecutionrole" {
  tags = {
    acse_component = "ECSTaskExecutionRole"
  }
}

resource "aws_iam_role" "microservicetaskrole" {
  tags = {
    acse_component = "MicroserviceTaskRole"
  }
}

resource "aws_db_instance" "rds_instance" {
  tags = {
    acse_component = "RDS Instance"
  }
}
