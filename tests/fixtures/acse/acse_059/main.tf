# ACSE-Eval IaC source path (dataset-relative):
# neuromorphic-computing-platform/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "awsinferentia" {
  tags = {
    acse_component = "AWSInferentia"
  }
}

resource "aws_resource" "awsparallelcluster" {
  tags = {
    acse_component = "AWSParallelCluster"
  }
}

resource "aws_resource" "batchcomputeenvironment" {
  tags = {
    acse_component = "BatchComputeEnvironment"
  }
}

resource "aws_resource" "inferencelayer" {
  tags = {
    acse_component = "InferenceLayer"
  }
}

resource "aws_s3_bucket" "inputdatabucket" {
  tags = {
    acse_component = "InputDataBucket"
  }
}

resource "aws_resource" "modelrepository" {
  tags = {
    acse_component = "ModelRepository"
  }
}

resource "aws_resource" "neuralprocessingengine" {
  tags = {
    acse_component = "NeuralProcessingEngine"
  }
}

resource "aws_resource" "performanceanalytics" {
  tags = {
    acse_component = "PerformanceAnalytics"
  }
}

resource "aws_resource" "sagemaker" {
  tags = {
    acse_component = "SageMaker"
  }
}

resource "aws_resource" "trainingenvironment" {
  tags = {
    acse_component = "TrainingEnvironment"
  }
}

resource "aws_instance" "traininginstances" {
  tags = {
    acse_component = "TrainingInstances"
  }
}
