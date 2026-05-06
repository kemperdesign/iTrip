from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import User, Message, AIResponse, Document
from app.middleware.auth import get_current_active_user
from app.services.guest_reply_service import generate_guest_reply
from app.schemas import (
    GenerateGuestReplyRequest,
    GenerateGuestReplyResponse,
    GuestMessageWithReply,
)
from app.utils.errors import NotFoundError, InternalServerError, log_error

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/guest-replies", tags=["guest_replies"])


@router.post("/generate", response_model=GenerateGuestReplyResponse)
async def generate_reply(
    request: GenerateGuestReplyRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Generate an AI-drafted reply to a guest message using templates and risk detection."""
    try:
        # Fetch the message
        message = db.query(Message).filter(Message.id == request.message_id).first()
        if not message:
            raise NotFoundError("Message", request.message_id)

        # Verify template doc exists if provided
        if request.template_doc_id:
            doc = db.query(Document).filter(Document.id == request.template_doc_id).first()
            if not doc:
                raise NotFoundError("Document", request.template_doc_id)

        # Generate reply using service
        result = generate_guest_reply(
            message_text=message.guest_message,
            template_doc_id=request.template_doc_id,
            ai_provider=request.ai_provider,
            include_templates=request.include_templates,
        )

        # Store in database
        ai_response = AIResponse(
            message_id=request.message_id,
            response_type="guest_reply",
            generated_content=result["reply_text"],
            ai_provider=result["ai_provider"],
            ai_model=result["ai_model"],
            user_id=current_user.id,
            approved_by_user=None,  # Not approved yet, just drafted
        )
        db.add(ai_response)
        db.commit()
        db.refresh(ai_response)

        return {
            "ai_response_id": ai_response.id,
            "reply_text": result["reply_text"],
            "risk_flags": result["risk_flags"],
            "source_templates": result["source_templates"],
            "ai_provider": result["ai_provider"],
            "ai_model": result["ai_model"],
            "requires_review": result["requires_review"],
        }
    except NotFoundError:
        raise
    except Exception as e:
        log_error("generate_reply", e)
        raise InternalServerError(f"Failed to generate reply: {str(e)}")


@router.get("/{message_id}", response_model=GuestMessageWithReply)
async def get_message_with_replies(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Fetch a guest message and all associated AI-generated replies."""
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        if not message:
            raise NotFoundError("Message", message_id)

        # Fetch all guest_reply responses for this message
        replies = db.query(AIResponse).filter(
            AIResponse.message_id == message_id,
            AIResponse.response_type == "guest_reply",
        ).all()

        # Format replies
        formatted_replies = [
            {
                "ai_response_id": reply.id,
                "reply_text": reply.generated_content,
                "risk_flags": [],  # Would need to re-detect or store, simplified here
                "source_templates": [],  # Would need to store separately
                "ai_provider": reply.ai_provider,
                "ai_model": reply.ai_model,
                "requires_review": reply.approved_by_user is None,
            }
            for reply in replies
        ]

        return {
            "message_id": message.id,
            "guest_name": message.guest_name,
            "guest_message": message.guest_message,
            "message_category": message.message_category,
            "risk_level": message.risk_level,
            "replies": formatted_replies,
        }
    except NotFoundError:
        raise
    except Exception as e:
        log_error("get_message_with_replies", e)
        raise InternalServerError(f"Failed to fetch message: {str(e)}")


@router.post("/{ai_response_id}/approve")
async def approve_reply(
    ai_response_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Approve an AI-drafted reply, marking it ready for sending."""
    try:
        ai_response = db.query(AIResponse).filter(
            AIResponse.id == ai_response_id,
            AIResponse.response_type == "guest_reply",
        ).first()

        if not ai_response:
            raise NotFoundError("AI Response", ai_response_id)

        # Mark as approved
        ai_response.approved_by_user = True
        db.commit()
        db.refresh(ai_response)

        return {
            "message": "Reply approved successfully",
            "error": False,
            "ai_response_id": ai_response.id,
            "approved_by": current_user.email,
        }
    except NotFoundError:
        raise
    except Exception as e:
        log_error("approve_reply", e)
        raise InternalServerError(f"Failed to approve reply: {str(e)}")
