output "s3_bucket_name" {
  description = "Name of the S3 bucket for document storage"
  value       = aws_s3_bucket.docuform_documents.bucket
}

output "sagemaker_execution_role_arn" {
  description = "SageMaker execution role ARN"
  value       = aws_iam_role.sagemaker_execution_role.arn
}

output "sagemaker_role_name" {
  description = "SageMaker execution role name"
  value       = aws_iam_role.sagemaker_execution_role.name
}
