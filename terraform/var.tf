variable "region" {
    default = "eu-west-1"
}
variable "AWS_ACCESS_KEY_ID" {}
variable "SECRET_ACCESS_KEY" {}

variable "vpc_id" {
  description = "Existing VPC to use (specify this, if you don't want to create new VPC)"
  type        = string
  default     = "vpc-0e42dfebfd2dc3e79"
}

variable "cidr" {
  description = "The CIDR block for the VPC. Default value is a valid CIDR, but not acceptable by AWS and should be overriden"
  type        = string
  default     = "172.31.0.0/16"
}

variable "db_username" {
  description = "Database administrator username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}

variable "pub_key"{
  description   = "public key ec2"
  type          = string
  sensitive     = true
}
