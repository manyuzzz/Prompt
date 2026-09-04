from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.conversation import Conversation, ChatMessage
from app.models.user import User
from app.middleware.auth import get_current_user
from app.services.ai.ai_service import ai_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


class SendMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


@router.get("/conversations")
async def get_conversations(current_user: User = Depends(get_current_user)):
    convos = await Conversation.find(
        Conversation.user_id == current_user.id,
        Conversation.is_archived == False
    ).sort(-Conversation.updated_at).limit(50).to_list()
    return {"success": True, "conversations": [
        {
            "id": str(c.id),
            "title": c.title,
            "last_message": c.last_message,
            "message_count": c.message_count,
            "updated_at": c.updated_at.isoformat(),
            "created_at": c.created_at.isoformat(),
        }
        for c in convos
    ]}


@router.get("/conversations/{conv_id}")
async def get_conversation(conv_id: str, current_user: User = Depends(get_current_user)):
    conv = await Conversation.get(conv_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"success": True, "conversation": {
        "id": str(conv.id),
        "title": conv.title,
        "messages": [{"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()} for m in conv.messages],
        "created_at": conv.created_at.isoformat(),
    }}


@router.post("/send")
async def send_message(body: SendMessageRequest, current_user: User = Depends(get_current_user)):
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if body.conversation_id:
        conv = await Conversation.get(body.conversation_id)
        if not conv or conv.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = Conversation(user_id=current_user.id)
        await conv.insert()

    conv.messages.append(ChatMessage(role="user", content=body.message))

    user_context = {
        "name": current_user.name,
        "target_role": current_user.target_role,
        "target_companies": current_user.target_companies,
        "skills": current_user.skills,
    }
    history = [{"role": m.role, "content": m.content} for m in conv.messages[:-1]]

    from app.services.ai.ai_service import ai_service
    SYSTEM_PROMPT = """You are an experienced placement mentor for engineering students in India. Help with technical subjects (DSA, DBMS, OS, Networks, OOP), aptitude preparation, resume advice, interview preparation, and career guidance. Use markdown formatting. Be specific and actionable."""

    if user_context.get("name"):
        SYSTEM_PROMPT += f"\nStudent: {user_context['name']}"
        if user_context.get("target_role"):
            SYSTEM_PROMPT += f", Target: {user_context['target_role']}"

    response = await ai_service.chat(
        history + [{"role": "user", "content": body.message}],
        SYSTEM_PROMPT,
    )

    conv.messages.append(ChatMessage(role="assistant", content=response))
    conv.update_meta()
    await conv.save()

    suggested = _get_suggestions(body.message)
    return {
        "success": True,
        "reply": response,
        "conversation_id": str(conv.id),
        "suggested_questions": suggested,
    }


@router.delete("/conversations/{conv_id}")
async def delete_conversation(conv_id: str, current_user: User = Depends(get_current_user)):
    conv = await Conversation.get(conv_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await conv.delete()
    return {"success": True, "message": "Conversation deleted"}


@router.get("/suggestions")
async def get_suggestions():
    suggestions = [
        "How should I prepare for TCS placement?",
        "Explain Binary Search Tree with operations",
        "What are the most asked SQL interview questions?",
        "How to write a strong resume for freshers?",
        "Tell me about yourself — best answer strategy",
        "Difference between process and thread in OS",
        "What is normalization in DBMS?",
        "Top 10 HR questions and best answers",
        "How to prepare for Amazon SDE interview?",
        "Explain OOPS concepts with examples",
        "What is dynamic programming? Explain with examples",
        "How to crack Infosys InfyTQ assessment?",
    ]
    import random
    return {"success": True, "suggestions": random.sample(suggestions, 6)}


def _get_suggestions(message: str) -> list:
    lower = message.lower()
    if any(w in lower for w in ["dsa", "array", "tree", "graph"]):
        return ["Explain dynamic programming", "Top tree problems", "Graph algorithms overview"]
    if any(w in lower for w in ["company", "tcs", "infosys", "amazon"]):
        return ["What is their aptitude pattern?", "Technical topics to focus", "Generate a roadmap"]
    if "resume" in lower:
        return ["How to write project descriptions?", "Skills to add", "ATS optimization"]
    if "interview" in lower or "hr" in lower:
        return ["Common HR questions", "Technical interview tips", "Behavioral question STAR method"]
    return ["How to prepare for TCS?", "Explain DSA concepts", "Resume improvement tips"]
