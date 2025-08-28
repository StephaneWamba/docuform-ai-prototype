variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "docuform-ai-prototype"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prototype"
}
