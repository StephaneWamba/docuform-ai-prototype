from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://localhost/docuform"

    # AWS
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "eu-central-1"
    s3_bucket_name: str = "docuform-ai-prototype-documents"

    # SageMaker
    sagemaker_endpoint_name: str = "docuform-qwen2vl-endpoint"

    # Application
    debug: bool = True
    secret_key: str = "your-secret-key-change-in-production"
    api_v1_str: str = "/api/v1"

    # OCR Settings
    max_file_size_mb: int = 10
    processing_timeout_seconds: int = 300

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
