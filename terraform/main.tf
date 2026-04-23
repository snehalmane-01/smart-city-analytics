terraform {
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "ml_artifacts" {
  bucket = "${var.project_name}-ml-artifacts"
}
