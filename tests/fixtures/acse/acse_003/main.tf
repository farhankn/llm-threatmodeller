# ACSE-Eval IaC source path (dataset-relative):
# aws-ai-chat-bot/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "all_aws_services" {
  tags = {
    acse_component = "All AWS Services"
  }
}

resource "aws_db_instance" "applicationloadbalancer" {
  tags = {
    acse_component = "ApplicationLoadBalancer"
  }
}

resource "aws_resource" "bedrockclaudemodel" {
  tags = {
    acse_component = "BedrockClaudeModel"
  }
}

resource "aws_resource" "cognitouserpool" {
  tags = {
    acse_component = "CognitoUserPool"
  }
}

resource "aws_lambda_function" "dataprocessinglambda" {
  tags = {
    acse_component = "DataProcessingLambda"
  }
}

resource "aws_db_instance" "dynamodbchathistory" {
  tags = {
    acse_component = "DynamoDBChatHistory"
  }
}

resource "aws_resource" "ecsfargateservice" {
  tags = {
    acse_component = "ECSFargateService"
  }
}

resource "aws_s3_bucket" "knowledgebasebucket" {
  tags = {
    acse_component = "KnowledgeBaseBucket"
  }
}

resource "aws_resource" "nextjswebapplication" {
  tags = {
    acse_component = "NextJSWebApplication"
  }
}

resource "aws_resource" "opensearchserverless" {
  tags = {
    acse_component = "OpenSearchServerless"
  }
}

resource "aws_resource" "securitygroups" {
  tags = {
    acse_component = "SecurityGroups"
  }
}

resource "aws_vpc" "vpc" {
  tags = {
    acse_component = "VPC"
  }
}

resource "aws_vpc" "vpcendpoints" {
  tags = {
    acse_component = "VPCEndpoints"
  }
}
