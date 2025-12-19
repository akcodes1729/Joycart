from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db import get_db
from app.models import Order

router = APIRouter()

@router.post("")
def payment(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status=="PAID":
        raise HTTPException(status_code=400, detail="Already Paid")
    order.status = "PAID"
    db.commit()

    return {
        "message": "payment successful",
        "order_id": order.id,
        "status": order.status
    }

@router.get("/success/{order_id}")
def payment_success(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "PAID":
        raise HTTPException(status_code=400, detail="Not Paid")

    return {
        "order_id": order.id,
        "status": order.status
    }

