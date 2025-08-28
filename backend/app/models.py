from sqlalchemy import Column, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500))
    document_type = Column(String(50), nullable=False)  # 'insurance_card' or 'intake_form'
    status = Column(String(20), nullable=False, default="uploaded")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

class Extraction(Base):
    __tablename__ = "extractions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    field_name = Column(String(100), nullable=False)
    extracted_value = Column(Text)
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    is_reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
