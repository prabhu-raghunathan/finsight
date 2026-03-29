from fastapi import APIRouter, HTTPException, Header
from typing import Annotated
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

from models.schemas import InsightRequest, InsightResponse
from clients.transaction_client import fetch_transactions
from services.insight_service import get_insight

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

router = APIRouter(prefix="/api/insights", tags=["insights"])


def extract_email(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/ask", response_model=InsightResponse)
async def ask_insight(
        request: InsightRequest,
        authorization: Annotated[str, Header()]
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.replace("Bearer ", "")
    extract_email(token)

    transactions = await fetch_transactions(token)

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    answer = await get_insight(transactions, request.question)

    return InsightResponse(question=request.question, answer=answer)