terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

# S3 Bucket for document storage
resource "aws_s3_bucket" "docuform_documents" {
  bucket = "docuform-ai-prototype-documents-${random_string.bucket_suffix.result}"

  tags = {
    Name        = "DocuForm Documents"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

resource "aws_s3_bucket_versioning" "docuform_versioning" {
  bucket = aws_s3_bucket.docuform_documents.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  lower   = true
  numeric = true
  special = false
}

# RDS PostgreSQL Database
resource "aws_db_instance" "docuform_db" {
  identifier             = "docuform-prototype-db"
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  storage_type           = "gp2"
  db_name                = "docuform"
  username               = "docuform_admin"
  password               = aws_secretsmanager_secret_version.db_password.secret_string
  parameter_group_name   = "default.postgres15"
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.docuform_subnet_group.name

  tags = {
    Name        = "DocuForm Prototype DB"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

# Database subnet group
resource "aws_db_subnet_group" "docuform_subnet_group" {
  name       = "docuform-db-subnet-group"
  subnet_ids = aws_subnet.docuform_private_subnets[*].id

  tags = {
    Name        = "DocuForm DB Subnet Group"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

# Secrets Manager for database password
resource "aws_secretsmanager_secret" "db_password" {
  name = "docuform-db-password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    password = "DocuForm2024Secure!"
  })
}

# VPC and Networking
resource "aws_vpc" "docuform_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "DocuForm VPC"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

resource "aws_subnet" "docuform_private_subnets" {
  count             = 2
  vpc_id            = aws_vpc.docuform_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name        = "DocuForm Private Subnet ${count.index + 1}"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

# Security Groups
resource "aws_security_group" "rds_sg" {
  name_prefix = "docuform-rds-"
  vpc_id      = aws_vpc.docuform_vpc.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app_sg.id]
  }

  tags = {
    Name        = "DocuForm RDS Security Group"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

resource "aws_security_group" "app_sg" {
  name_prefix = "docuform-app-"
  vpc_id      = aws_vpc.docuform_vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "DocuForm App Security Group"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

# IAM Role for SageMaker
resource "aws_iam_role" "sagemaker_execution_role" {
  name = "docuform-sagemaker-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "DocuForm SageMaker Role"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

resource "aws_iam_role_policy_attachment" "sagemaker_full_access" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

# Elastic Beanstalk Application
resource "aws_elastic_beanstalk_application" "docuform_app" {
  name        = "docuform-ai-prototype"
  description = "Healthcare Patient Intake OCR System"

  tags = {
    Name        = "DocuForm Application"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

# Internet Gateway for VPC
resource "aws_internet_gateway" "docuform_igw" {
  vpc_id = aws_vpc.docuform_vpc.id

  tags = {
    Name        = "DocuForm Internet Gateway"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

# Route Table
resource "aws_route_table" "docuform_route_table" {
  vpc_id = aws_vpc.docuform_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.docuform_igw.id
  }

  tags = {
    Name        = "DocuForm Route Table"
    Environment = "prototype"
    Project     = "docuform-ai"
  }
}

resource "aws_route_table_association" "docuform_rta" {
  count          = 2
  subnet_id      = aws_subnet.docuform_private_subnets[count.index].id
  route_table_id = aws_route_table.docuform_route_table.id
}
