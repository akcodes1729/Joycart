from sqlalchemy.orm import Session
from app.db.models import Cart, Product, Checkout, CheckoutItem
import uuid

def create_checkout_from_cart(current_user, db: Session):
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart or not cart.items:
        raise ValueError("Cart is empty")

    product_ids = [item.product_id for item in cart.items]
    products = db.query(Product).filter(
        Product.id.in_(product_ids)
    ).all()

    product_map = {p.id: p for p in products}

    total_amount = 0
    for item in cart.items:
        product = product_map[item.product_id]

        if product.stock < item.quantity:
            raise ValueError("Insufficient stock")

        total_amount += product.price * item.quantity

    checkout = Checkout(
        checkout_id=str(uuid.uuid4()),
        user_id=current_user.id,
        amount=total_amount,
        mode="CART",
        status="CREATED"
    )

    db.add(checkout)
    db.flush()

    for item in cart.items:
        product = product_map[item.product_id]
        db.add(
            CheckoutItem(
                checkout_id=checkout.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_checkout=product.price
            )
        )

    db.commit()
    return checkout