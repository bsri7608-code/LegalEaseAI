from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from gemini_generator import GeminiDocumentGenerator

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=4000)
    terms: str = Field(..., min_length=2, max_length=12000)
    effective_date: str = Field(..., min_length=2, max_length=80)

    @field_validator("document_type", "parties", "terms", "effective_date")
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class DocumentResponse(BaseModel):
    document_type: str
    content: str


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()
        content = generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.effective_date,
        )
        return DocumentResponse(document_type=request.document_type, content=content)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"Document generation failed: {exc}"
        ) from exc
