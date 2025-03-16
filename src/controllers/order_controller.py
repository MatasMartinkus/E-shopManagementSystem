from src.utils.dbengine import get_db
from src.models.order import Order, OrderProduct
from sqlalchemy.orm import joinedload
from src.models.financial import Financial
from datetime import datetime
from sqlalchemy import cast, String

class OrderController:
    def add_order(self, customer_id, cart):
        with get_db() as db:
            order = Order(customer_id=customer_id)
            db.add(order)
            db.commit()
            db.refresh(order)

            total_amount = 0
            for product, quantity in cart:
                order_product = OrderProduct(
                    order_id=order.id,
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=quantity
                )
                db.add(order_product)
                total_amount += product.price * quantity
            db.commit()

            # Generate receipt
            receipt = Financial(
                transaction_date=datetime.utcnow(),
                amount=total_amount,
                transaction_type='Income',
                recipient=f'Customer ID: {customer_id}',
                sender='E-Shop'
            )
            db.add(receipt)
            db.commit()

            return order

    def edit_order(self, order_id, customer_id=None, date_created=None):
        with get_db() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return None
            if customer_id:
                order.customer_id = customer_id
            if date_created:
                order.date_created = date_created
            db.commit()
            db.refresh(order)
            return order

    def add_product_to_order(self, order_id, product_id, quantity, name, price):
        with get_db() as db:
            order_product = OrderProduct(order_id=order_id, product_id=product_id, quantity=quantity, name=name, price=price)
            db.add(order_product)
            db.commit()
            db.refresh(order_product)
            return order_product

    def remove_product_from_order(self, order_id, product_id):
        with get_db() as db:
            order_product = db.query(OrderProduct).filter(OrderProduct.order_id == order_id, OrderProduct.product_id == product_id).first()
            if not order_product:
                return None
            db.delete(order_product)
            db.commit()
            return order_product

    def update_product_quantity_in_order(self, order_id, product_id, quantity):
        with get_db() as db:
            order_product = db.query(OrderProduct).filter(OrderProduct.order_id == order_id, OrderProduct.product_id == product_id).first()
            if not order_product:
                return None
            order_product.quantity = quantity
            db.commit()
            db.refresh(order_product)
            return order_product

    def get_all_orders(self):
        with get_db() as db:
            return db.query(Order).options(joinedload(Order.products)).all()

    def delete_order(self, order_id):
        with get_db() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                db.query(OrderProduct).filter(OrderProduct.order_id == order_id).delete()
                db.delete(order)
                db.commit()

    def get_order_by_id(self, order_id):
        with get_db() as db:
            return db.query(Order).options(joinedload(Order.products)).filter(Order.id == order_id).first()

    def search_orders(self, search_term, filter_by):
        with get_db() as db:
            query = db.query(Order).options(joinedload(Order.products))
            if filter_by == "Date Created":
                query = query.filter(cast(Order.date_created, String).ilike(f"%{search_term}%"))
            elif filter_by == "Customer ID":
                query = query.filter(Order.customer_id.ilike(f"%{search_term}%"))
            elif filter_by == "Product ID":
                query = query.join(Order.products).filter(OrderProduct.product_id.ilike(f"%{search_term}%"))
            return query.all()