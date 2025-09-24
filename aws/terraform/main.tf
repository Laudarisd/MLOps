# main.tf
# Sample Terraform configuration for AWS infrastructure
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "mlops_bucket" {
  bucket = "mlops-sample-bucket"
  acl    = "private"
}
