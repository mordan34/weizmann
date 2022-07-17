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
  region = "us-east-1"
}

resource "aws_instance" "webapp1" {
  ami           = "ami-0cff7528ff583bf9a"
  instance_type = "t2.micro"

  tags = {
    Name = "webapp1"
    Type = "WEB"
  }
}
