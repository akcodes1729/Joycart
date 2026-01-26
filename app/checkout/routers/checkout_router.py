from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.auth import get_current_user
from app.db.models import User
from app.checkout.services.checkout_services import (lazy_cleanup_checkouts,cart_checkout,buy_now_checkout,
get_addresses,get_checkout,shipping_address,get_checkout_items,create_payonline_order)



router = APIRouter()
pages_router = APIRouter()

templates = Jinja2Templates(directory="templates")



@router.post("/checkout/start")
def start_checkout(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    checkout_id = cart_checkout(
        db=db,
        current_user=current_user
    )

    return {
        "redirect_url": f"/checkout/address?checkout_id={checkout_id}"
    }

@router.post("/checkout/buy-now")
def buy_now(
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    checkout_id = buy_now_checkout(
        db=db,
        current_user=current_user,
        product_id=product_id,
        quantity=quantity
    )

    return {
        "redirect_url": f"/checkout/address?checkout_id={checkout_id}"
    }



@pages_router.get("/checkout/address")
def checkout_address_page(
    request: Request,
    checkout_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    get_checkout(
        db=db,
        checkout_id=checkout_id,
        user_id=current_user.id
    )

    
    addresses = get_addresses(
        db=db,
        user_id=current_user.id,
        selected_address_id = None
    )

    return templates.TemplateResponse(
        "checkout_delivery_address.html",
        {
            "request": request,
            "addresses": addresses,
            "checkout_id": checkout_id,
            "current_user": current_user
        }
    )

@router.post("/checkout/address")
def save_checkout_address(
    checkout_id: str = Form(...),
    selected_address_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
 

    checkout = get_checkout(
        db=db,
        checkout_id=checkout_id,
        user_id=current_user.id
    )

    address = get_addresses(
        db=db,
        user_id=current_user.id,
        selected_address_id = selected_address_id
    )

    shipping_address(db,checkout,address)

    return RedirectResponse(
        f"/checkout/summary?checkout_id={checkout_id}",
        status_code=302
    )

@pages_router.get("/checkout/summary")
def checkout_summary(
    request: Request,
    checkout_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lazy_cleanup_checkouts(db)

    checkout = get_checkout(
        db=db,
        checkout_id=checkout_id,
        user_id=current_user.id
    )

    items = get_checkout_items(db,checkout)

    return templates.TemplateResponse(
        "checkout_summary.html",
        {
            "request": request,
            "checkout": checkout,
            "items": items,
            "checkout_id": checkout_id,
            "current_user":current_user
        }
    )

    
             

@router.post("/checkout/confirm")
def confirm_checkout(
    checkout_id: str = Form(...),
    db: Session = Depends(get_db)
):
    
    return RedirectResponse(
        f"/checkout/payment?checkout_id={checkout_id}",
        status_code=302
    )


@pages_router.get("/checkout/payment")
def checkout_payment_page(
    request: Request,
    checkout_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lazy_cleanup_checkouts(db)
    
    checkout = get_checkout(
        db=db,
        checkout_id=checkout_id,
        user_id=current_user.id
    )

    return templates.TemplateResponse(
        "checkout_payment.html",
        {
            "request": request,
            "checkout_id": checkout_id,
            "amount": checkout.amount,
            "current_user":current_user
        }
    )



@router.post("/checkout/payment")
def select_payment_method(
    checkout_id: str = Form(...),
    method: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

   
    get_checkout(
        db=db,
        checkout_id=checkout_id,
        user_id=current_user.id
    )


    if method == "COD":
        return RedirectResponse(
            f"/checkout/cod/confirm?checkout_id={checkout_id}",
            status_code=302
        )

    return RedirectResponse(
        f"/checkout/payonline?checkout_id={checkout_id}",
        status_code=302
    )

@pages_router.get("/checkout/payonline")
def payonline(
    request:Request,
    checkout_id: str,
):
    return templates.TemplateResponse(
        "payonline_gateway.html",{
            "request":request,
            "checkout_id":checkout_id         
        }
    )


@router.post("/checkout/payonline/create")
def create_payonline_checkout(
    checkout_id: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_payonline_order(
        db=db,
        checkout_id=checkout_id,
        user_id=current_user.id
    )

@pages_router.get("/checkout/payonline/waiting")
def payonline_waiting_page(
    request: Request
):
    return templates.TemplateResponse(
        "payonline_success.html",
        {
            "request": request
        }
    )

