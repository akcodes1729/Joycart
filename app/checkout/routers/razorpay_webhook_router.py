import hmac,os,hashlib
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.checkout.services.razorpay_webhook_service import handle_razorpay_event
router = APIRouter()


RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")

@router.post("/checkout/payonline/webhook")
async def razorpay_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")

    expected_signature = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not signature or not hmac.compare_digest(
        signature, expected_signature
    ):
        return {"status": "ignored"}

    return handle_razorpay_event(db=db, body=body)
