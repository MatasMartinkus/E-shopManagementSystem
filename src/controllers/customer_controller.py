from src.utils.dbengine import get_db
from src.models.customer import Customer
from src.models.user import User
from sqlalchemy.orm import joinedload
import random
import string

class CustomerController:
    def add_customer(self, name, last_name, address, user_id, phone):
        with get_db() as db:
            customer = Customer(name=name, last_name=last_name, 
                                phone=phone, address=address, user_id=user_id, 
                                reference_code=self.generate_reference_code())
            db.add(customer)
            db.commit()
            db.refresh(customer)
            return customer

    def get_customer_by_id(self, customer_id):
        with get_db() as db:
            return db.query(Customer).options(joinedload(Customer.user)).filter(Customer.id == customer_id).first()

    def get_customer_by_user_id(self, user_id):
        with get_db() as db:
            return db.query(Customer).options(joinedload(Customer.user)).filter(Customer.user_id == user_id).first()

    def edit_customer(self, customer_id, name, last_name, email=None, phone=None, address=None):
        with get_db() as db:
            customer = db.query(Customer).options(joinedload(Customer.user)).filter(Customer.id == customer_id).first()
            if not customer:
                return None
            if name:
                customer.name = name
            if last_name:
                customer.last_name = last_name
            if email:
                user = db.query(User).filter(User.id == customer.user_id).first()
                if user:
                    user.email = email
            if address:
                customer.address = address
            if phone:
                customer.phone = phone
            db.commit()
            db.refresh(customer)
            return customer

    def get_all_customers(self):
        with get_db() as db:
            return db.query(Customer).options(joinedload(Customer.user)).all()

    def delete_customer(self, customer_id):
        with get_db() as db:
            customer = db.query(Customer).options(joinedload(Customer.user)).filter(Customer.id == customer_id).first()
            if customer:
                db.delete(customer)
                db.commit()
    
    def search_customers(self, search_term, filter_by):
        with get_db() as db:
            query = db.query(Customer).options(joinedload(Customer.user))
            if filter_by == "Name":
                query = query.filter(Customer.name.ilike(f"%{search_term}%"))
            elif filter_by == "Last Name":
                query = query.filter(Customer.last_name.ilike(f"%{search_term}%"))
            elif filter_by == "Email":
                query = query.join(Customer.user).filter(User.email.ilike(f"%{search_term}%"))
            
            return query.all()
        
    def generate_reference_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
