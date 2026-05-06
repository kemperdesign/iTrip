from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import User, Document, DocumentChunk
from app.middleware.auth import get_current_active_user
from app.schemas import DocumentUploadResponse
from app.services.file_processor import process_file, validate_file
from app.services.embeddings import (
    chunk_text,
    create_embeddings_batch,
    store_chunks_in_qdrant,
)
from app.config import settings
from app.utils.errors import (
    ValidationError,
    NotFoundError,
    ConflictError,
    InternalServerError,
    log_error,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Upload and process a document (DOCX, XLSX, PDF)."""
    try:
        if not file.filename:
            raise ValidationError("File must have a name")

        file_content = await file.read()
        file_size = len(file_content)

        if not validate_file(file.filename, file_size):
            raise ValidationError(
                f"File must be one of {settings.allowed_file_types} and under {settings.max_file_size_mb}MB"
            )

        try:
            doc_type, extracted_text, file_hash = process_file(file_content, file.filename)
        except ValueError as e:
            raise ValidationError(f"Failed to parse file: {str(e)}")

        existing_doc = db.query(Document).filter(Document.file_hash == file_hash).first()
        if existing_doc:
            raise ConflictError("Document", "This file has already been uploaded")

        document = Document(
            filename=file.filename,
            document_type=doc_type,
            content=extracted_text,
            file_hash=file_hash,
            uploaded_by=current_user.id,
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        try:
            chunks = chunk_text(extracted_text)
            embeddings = create_embeddings_batch(chunks)
            vector_ids = store_chunks_in_qdrant(document.id, chunks, embeddings)

            for chunk_idx, (chunk, vector_id) in enumerate(zip(chunks, vector_ids)):
                doc_chunk = DocumentChunk(
                    document_id=document.id,
                    chunk_index=chunk_idx,
                    chunk_text=chunk,
                    qdrant_vector_id=vector_id,
                )
                db.add(doc_chunk)

            db.commit()
        except Exception as e:
            db.delete(document)
            db.commit()
            log_error("upload_document - create_embeddings", e)
            raise InternalServerError(f"Failed to create embeddings: {str(e)}")

        return {
            "id": document.id,
            "filename": document.filename,
            "document_type": document.document_type,
            "status": "indexed",
            "chunk_count": len(chunks),
            "created_at": document.created_at,
        }
    except (ValidationError, ConflictError, InternalServerError):
        raise
    except Exception as e:
        log_error("upload_document", e)
        raise InternalServerError(f"Failed to upload document: {str(e)}")


@router.get("/")
async def list_documents(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """List all uploaded documents."""
    documents = db.query(Document).all()

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "document_type": doc.document_type,
            "uploaded_by": doc.uploaded_by,
            "chunk_count": db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).count(),
            "created_at": doc.created_at,
        }
        for doc in documents
    ]


@router.get("/{doc_id}")
async def get_document(
    doc_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get document details."""
    try:
        document = db.query(Document).filter(Document.id == doc_id).first()

        if not document:
            raise NotFoundError("Document", doc_id)

        chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_id).all()

        return {
            "id": document.id,
            "filename": document.filename,
            "document_type": document.document_type,
            "uploaded_by": document.uploaded_by,
            "chunk_count": len(chunks),
            "content_preview": document.content[:500] + "..." if len(document.content) > 500 else document.content,
            "created_at": document.created_at,
        }
    except NotFoundError:
        raise
    except Exception as e:
        log_error("get_document", e)
        raise InternalServerError(f"Failed to retrieve document: {str(e)}")


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete a document and its embeddings."""
    try:
        document = db.query(Document).filter(Document.id == doc_id).first()

        if not document:
            raise NotFoundError("Document", doc_id)

        chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_id).all()

        for chunk in chunks:
            db.delete(chunk)

        db.delete(document)
        db.commit()

        return {"message": "Document deleted successfully", "error": False}
    except NotFoundError:
        raise
    except Exception as e:
        db.rollback()
        log_error("delete_document", e)
        raise InternalServerError(f"Failed to delete document: {str(e)}")
