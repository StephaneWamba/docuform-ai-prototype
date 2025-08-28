from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    INSURANCE_CARD = "insurance_card"
    INTAKE_FORM = "intake_form"

class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Document schemas
class DocumentBase(BaseModel):
    filename: str = Field(..., description="Original filename")
    document_type: DocumentType = Field(..., description="Type of document")

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: str = Field(..., description="Document UUID")
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED)
    created_at: datetime = Field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Extraction schemas
class ExtractionBase(BaseModel):
    field_name: str = Field(..., description="Extracted field name")
    extracted_value: Optional[str] = Field(None, description="Extracted value")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")

class ExtractionCreate(ExtractionBase):
    document_id: str = Field(..., description="Associated document ID")

class Extraction(ExtractionBase):
    id: str = Field(..., description="Extraction UUID")
    document_id: str
    is_reviewed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

# Patient data schemas
class PatientInfo(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    insurance_provider: Optional[str] = None
    policy_number: Optional[str] = None
    subscriber_id: Optional[str] = None
    email_address: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_record_number: Optional[str] = None
    primary_care_physician: Optional[str] = None

# API response schemas
class ProcessingResponse(BaseModel):
    document_id: str
    status: str
    message: str
    estimated_time: Optional[int] = None

class ExtractionResult(BaseModel):
    document_id: str
    patient_info: PatientInfo
    processing_time: float
    overall_confidence: float

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
