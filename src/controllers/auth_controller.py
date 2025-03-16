import bcrypt
from src.utils.dbengine import get_db
from src.models.user import User
from src.models.customer import Customer

class AuthController:
    PERMISSIONS = ["I", "II", "III", "IV"]
    DEPARTMENTS = ["sales", "marketing", "finance", "hr", "it", "operations"]
    def __init__(self, email_controller, customer_controller, admin_controller, manager_controller):
        self.manager_controller = manager_controller
        self.admin_controller = admin_controller
        self.customer_controller = customer_controller
        self.email_controller = email_controller


    def get_password_hash(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def register_user(self, username: str, email: str, password: str,
                      role=None):
        with get_db() as db:
            hashed_password = self.get_password_hash(password)
            user = User(username=username, email=email, hashed_password=hashed_password, role=role)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def register_user_additional(self, user, permissions=None, department=None, name=None, last_name=None,
                      role=None, address=None, phone=None, location=None):
        if role == "customer":
            return self.customer_controller.add_customer(name=name, last_name=last_name, address=address, 
                                                            user_id=user.id, phone=phone)
                
        elif role == "admin":
            return self.admin_controller.add_admin(department=department, user_id=user.id, permissions=permissions)
        
        elif role == "manager":
            return self.manager_controller.add_manager(location=location, permissions=permissions, user_id=user.id)


    def authenticate_user(self, username, password):
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            if user and self.verify_password(password, user.hashed_password):
                return user
        return None
    
    def get_all_permissions(self):
        return self.PERMISSIONS
    
    def get_all_departments(self):
        return self.DEPARTMENTS