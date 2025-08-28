from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import documents, extractions

app = FastAPI(
    title="DocuForm AI - Healthcare OCR API",
    description="AI-powered document processing for healthcare patient intake",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(extractions.router, prefix="/api/v1/extractions", tags=["extractions"])

@app.get("/")
async def root():
    return {"message": "DocuForm AI Healthcare OCR API", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "docuform-ai"}
