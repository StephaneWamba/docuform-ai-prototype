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

# S3 Bucket for document storage (Railway backend will use this)
resource "aws_s3_bucket" "docuform_documents" {
  bucket = lower("docuform-ai-prototype-documents-${random_string.bucket_suffix.result}")

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

# IAM Role for SageMaker (for OCR processing)
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

# Add S3 access to SageMaker role
resource "aws_iam_role_policy_attachment" "sagemaker_s3_access" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
