from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..schemas import Extraction, ExtractionResult, PatientInfo
from ..models import Extraction as ExtractionModel, Document
from ..database import get_db

router = APIRouter()


@router.get("/{document_id}", response_model=ExtractionResult)
async def get_extraction_result(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get extraction results for a document
    """
    # Check if document exists
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get all extractions for this document
    extractions = db.query(ExtractionModel).filter(
        ExtractionModel.document_id == document_id
    ).all()

    if not extractions:
        raise HTTPException(
            status_code=404, detail="No extractions found for this document")

    # Build patient info from extractions
    patient_info = PatientInfo()
    total_confidence = 0.0

    for extraction in extractions:
        value = extraction.extracted_value
        confidence = extraction.confidence_score
        total_confidence += confidence

        if extraction.field_name == "full_name":
            patient_info.full_name = value
        elif extraction.field_name == "date_of_birth":
            patient_info.date_of_birth = value
        elif extraction.field_name == "gender":
            patient_info.gender = value
        elif extraction.field_name == "phone_number":
            patient_info.phone_number = value
        elif extraction.field_name == "address":
            patient_info.address = value
        elif extraction.field_name == "insurance_provider":
            patient_info.insurance_provider = value
        elif extraction.field_name == "policy_number":
            patient_info.policy_number = value
        elif extraction.field_name == "subscriber_id":
            patient_info.subscriber_id = value
        elif extraction.field_name == "email_address":
            patient_info.email_address = value
        elif extraction.field_name == "emergency_contact":
            patient_info.emergency_contact = value
        elif extraction.field_name == "medical_record_number":
            patient_info.medical_record_number = value
        elif extraction.field_name == "primary_care_physician":
            patient_info.primary_care_physician = value

    # Calculate overall confidence
    overall_confidence = total_confidence / \
        len(extractions) if extractions else 0.0

    return ExtractionResult(
        document_id=document_id,
        patient_info=patient_info,
        processing_time=0.0,  # TODO: Calculate actual processing time
        overall_confidence=round(overall_confidence, 2)
    )


@router.get("/{document_id}/details", response_model=List[Extraction])
async def get_extraction_details(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed extraction information for a document
    """
    # Check if document exists
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    extractions = db.query(ExtractionModel).filter(
        ExtractionModel.document_id == document_id
    ).all()

    return [Extraction.from_orm(extraction) for extraction in extractions]
