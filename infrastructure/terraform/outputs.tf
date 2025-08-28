output "s3_bucket_name" {
  description = "Name of the S3 bucket for document storage"
  value       = aws_s3_bucket.docuform_documents.bucket
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.docuform_db.endpoint
  sensitive   = true
}

output "rds_database_name" {
  description = "RDS database name"
  value       = aws_db_instance.docuform_db.db_name
}

output "rds_username" {
  description = "RDS username"
  value       = aws_db_instance.docuform_db.username
  sensitive   = true
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.docuform_vpc.id
}

output "elastic_beanstalk_application_name" {
  description = "Elastic Beanstalk application name"
  value       = aws_elastic_beanstalk_application.docuform_app.name
}

output "sagemaker_execution_role_arn" {
  description = "SageMaker execution role ARN"
  value       = aws_iam_role.sagemaker_execution_role.arn
}
