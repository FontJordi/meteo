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

locals {
  create_vpc = var.vpc_id == ""
}

data "aws_vpc" "selected" {
  count = local.create_vpc ? 0 : 1

  id = var.vpc_id
}

resource "aws_vpc" "this" {
  count = local.create_vpc ? 1 : 0

  cidr_block = var.cidr
}

resource "aws_db_instance" "terraformdb" {
  allocated_storage    = 20
  db_name              = "mydb"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = "db.t3.micro"
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true
  publicly_accessible  = true 
}

