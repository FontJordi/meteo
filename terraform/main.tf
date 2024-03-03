terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
  }
 }
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

resource "tls_private_key" "pk" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "devkey" {
  key_name   = "myKey"
  public_key =  tls_private_key.pk.public_key_openssh

  provisioner "local-exec" { # Create a "myKey.pem" to your computer!!
    command = "echo '${tls_private_key.pk.private_key_pem}' > ./myKey.pem"
  }
}

data "aws_ami" "amzn-linux-2023-ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_instance" "first_instance" {
  ami           = data.aws_ami.amzn-linux-2023-ami.id
  instance_type = "t2.micro"
  key_name      = "myKey"


  depends_on = [ aws_key_pair.devkey ]
}
