# ACSE-Eval IaC source path (dataset-relative):
# datazone-arch/cdk/
# Terraform source files were not available under this path.
# Synthetic resource stubs generated from affected components:

resource "aws_resource" "auroracluster" {
  tags = {
    acse_component = "AuroraCluster"
  }
}

resource "aws_instance" "dmsreplicationinstance" {
  tags = {
    acse_component = "DMSReplicationInstance"
  }
}

resource "aws_iam_role" "datazoneservicerole" {
  tags = {
    acse_component = "DataZoneServiceRole"
  }
}

resource "aws_vpc" "datazonevpc" {
  tags = {
    acse_component = "DataZoneVpc"
  }
}

resource "aws_resource" "defaultsg" {
  tags = {
    acse_component = "DefaultSG"
  }
}

resource "aws_s3_bucket" "firehosetos3role" {
  tags = {
    acse_component = "FirehoseToS3Role"
  }
}

resource "aws_iam_role" "gluecrawlerrole" {
  tags = {
    acse_component = "GlueCrawlerRole"
  }
}

resource "aws_db_instance" "gluedatabase" {
  tags = {
    acse_component = "GlueDatabase"
  }
}

resource "aws_resource" "gluejob" {
  tags = {
    acse_component = "GlueJob"
  }
}

resource "aws_iam_role" "gluejobrole" {
  tags = {
    acse_component = "GlueJobRole"
  }
}

resource "aws_resource" "redshiftcluster" {
  tags = {
    acse_component = "RedshiftCluster"
  }
}

resource "aws_s3_bucket" "s3datalakecrawler" {
  tags = {
    acse_component = "S3DataLakeCrawler"
  }
}

resource "aws_db_instance" "aws-rds" {
  tags = {
    acse_component = "aws-rds"
  }
}

resource "aws_resource" "aws-redshift" {
  tags = {
    acse_component = "aws-redshift"
  }
}
