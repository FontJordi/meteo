terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
    access_key = var.AWS_ACCESS_KEY_ID
    secret_key = var.SECRET_ACCESS_KEY
    region = var.region
}

resource "aws_s3_bucket" "meteobucket" {
  bucket = "meteobucketfirst"
}