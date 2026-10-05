import os
import stripe
from fastapi import Request
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.dependencies import get_current_user
from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderResponse
from app.services.stripe_service import create_checkout_session
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0

    order = Order(
        user_id=current_user.id,
        total_amount=0,
        payment_status="PENDING",
    )

    db.add(order)
    db.flush()

    response_items = []

    for item in cart.items:
        subtotal = item.product.price * item.quantity
        total_amount += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price,
        )

        db.add(order_item)

        response_items.append({
            "product_id": item.product.id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": item.product.price,
            "subtotal": subtotal,
        })

    order.total_amount = total_amount

    for item in list(cart.items):
        db.delete(item)

    db.commit()
    db.refresh(order)

    return {
        "id": order.id,
        "total_amount": order.total_amount,
        "payment_status": order.payment_status,
        "items": response_items,
    }


@router.get("/")
def get_orders(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Order).filter(
        Order.user_id == current_user.id
    )

    total = query.count()

    orders = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    result = []

    for order in orders:
        items = []

        for item in order.items:
            items.append({
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.price * item.quantity,
            })

        result.append({
            "id": order.id,
            "total_amount": order.total_amount,
            "payment_status": order.payment_status,
            "items": items,
        })

    return {
        "items": result,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
    }

@router.post("/{order_id}/checkout")
def checkout_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.payment_status == "PAID":
        raise HTTPException(
            status_code=400,
            detail="Order is already paid"
        )

    session = create_checkout_session(order)

    return {
        "checkout_url": session.url,
        "session_id": session.id,
    }

@router.get("/admin/all")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    orders = db.query(Order).all()

    result = []

    for order in orders:
        result.append({
            "id": order.id,
            "user_id": order.user_id,
            "total_amount": order.total_amount,
            "payment_status": order.payment_status,
        })

    return {
        "items": result,
        "total": len(result)
    }

@router.get("/admin/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    total_users = db.query(User).count()

    total_products = db.query(Product).filter(
        Product.is_active == 1
    ).count()

    total_orders = db.query(Order).count()

    total_revenue = sum(
        order.total_amount
        for order in db.query(Order).filter(
            Order.payment_status == "PAID"
        ).all()
    )

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
    }

from sqlalchemy import func

@router.get("/admin/reports/revenue")
def revenue_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    report = (
        db.query(
            Order.payment_status,
            func.sum(Order.total_amount).label("total_revenue")
        )
        .group_by(Order.payment_status)
        .all()
    )

    return [
        {
            "payment_status": status,
            "total_revenue": total or 0
        }
        for status, total in report
    ]

@router.get("/admin/reports/orders-by-user")
def orders_by_user_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    report = (
        db.query(
            Order.user_id,
            func.count(Order.id).label("order_count")
        )
        .group_by(Order.user_id)
        .all()
    )

    return [
        {
            "user_id": user_id,
            "order_count": order_count
        }
        for user_id, order_count in report
    ]

@router.get("/admin/reports/orders-by-product")
def orders_by_product_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    report = (
        db.query(
            OrderItem.product_id,
            func.sum(OrderItem.quantity).label("total_quantity")
        )
        .group_by(OrderItem.product_id)
        .all()
    )

    return [
        {
            "product_id": product_id,
            "total_quantity": total_quantity
        }
        for product_id, total_quantity in report
    ]

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid webhook"
        )

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        order_id = session["metadata"].get("order_id")

        if order_id:
            db = SessionLocal()

            try:
                order = db.query(Order).filter(
                    Order.id == int(order_id)
                ).first()

                if order:
                    order.payment_status = "PAID"
                    db.commit()
            finally:
                db.close()

    return {"message": "Webhook received"}