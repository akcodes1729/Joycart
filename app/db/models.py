from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float,Boolean,JSON,Numeric
from app.db.db import Base
from sqlalchemy.orm import relationship
from datetime import datetime,timedelta


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) 
    is_seller = Column(Boolean, default=False)
    seller_id = Column(Integer, unique=True, nullable=True)
    role = Column(String, default="user")
    is_blocked = Column(Boolean, default=False)

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)          
    phone = Column(String, nullable=False)

    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True)

    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(String, nullable=False)

    is_default = Column(Boolean, default=False)

    user = relationship("User", backref="addresses")

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    store_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    price = Column(Numeric(10, 2))
    discountPercentage = Column(Float)
    rating = Column(Float)
    stock = Column(Integer)
    brand = Column(String,nullable=True)
    sku = Column(String, unique=True, index=True)
    weight = Column(Integer)
    dimensions = Column(JSON, nullable=True)
    warrantyInformation = Column(String)
    shippingInformation = Column(String)
    availabilityStatus = Column(String)
    returnPolicy = Column(String)
    thumbnail = Column(String)
    images = Column(JSON, nullable=False) 
    reviews = relationship("Review", back_populates="product")

class Checkout(Base):
    __tablename__ = "checkouts"

    id = Column(Integer, primary_key=True)
    checkout_id = Column(String, unique=True, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    mode = Column(String) 

    shipping_address = Column(JSON, nullable=True)

    amount = Column(Numeric(10, 2), nullable=False)

    status = Column(String,default="CREATED",nullable=False)

    gateway_order_id = Column(String, unique=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(minutes=15)
    )   

class CheckoutItem(Base):
    __tablename__ = "checkout_items"

    id = Column(Integer, primary_key=True, index=True)

    checkout_id = Column(
        ForeignKey("checkouts.id", ondelete="CASCADE"),
        nullable=False
    )

    product_id = Column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)
    price_at_checkout = Column(Numeric(10, 2), nullable=False)
     
    product = relationship("Product")
 

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    checkout_id = Column(String, unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    shipping_address = Column(JSON,nullable=True)


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="PLACED",nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    items = relationship("CartItem",back_populates="cart",cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")
                        
    
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False) # success | failed
    method = Column(String, nullable=False)
    gateway_payment_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.id"))
    orderitem_id = Column(Integer, ForeignKey("order_items.id"), index=True)
    amount = Column(Numeric(10, 2))
    reason = Column(String)
    status = Column(String)
    gateway_payment_id = Column(String, nullable=True)
    gateway_refund_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    product = relationship("Product", back_populates="reviews")
    created_at = Column(DateTime, default=datetime.utcnow)




