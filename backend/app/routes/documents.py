from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from ..schemas import Document, DocumentCreate, ProcessingResponse
from ..models import Document as DocumentModel
from ..database import get_db

router = APIRouter()

@router.post("/upload", response_model=ProcessingResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "insurance_card",
    db: Session = Depends(get_db)
):
    """
    Upload a document for OCR processing
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed. Allowed types: {', '.join(allowed_types)}"
        )

    # Validate file size (10MB limit)
    file_content = await file.read()
    file_size_mb = len(file_content) / (1024 * 1024)
    if file_size_mb > 10:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

    # Create document record
    document_id = str(uuid.uuid4())
    document_data = DocumentCreate(
        filename=file.filename,
        document_type=document_type
    )

    db_document = DocumentModel(
        id=document_id,
        filename=document_data.filename,
        document_type=document_data.document_type,
        status="uploaded"
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # TODO: Upload file to S3
    # TODO: Trigger OCR processing

    return ProcessingResponse(
        document_id=document_id,
        status="uploaded",
        message="Document uploaded successfully",
        estimated_time=30
    )

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get document information by ID
    """
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return Document.from_orm(document)

@router.get("/", response_model=List[Document])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all documents with pagination
    """
    documents = db.query(DocumentModel).offset(skip).limit(limit).all()
    return [Document.from_orm(doc) for doc in documents]
