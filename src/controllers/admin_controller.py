from src.utils.dbengine import get_db
from src.models.admin import Admin

class AdminController:
    def add_admin(self, department, permissions, user_id):
        try:
            with get_db() as db:
                admin = Admin(user_id=user_id, department=department, permissions=permissions)
                db.add(admin)
                db.commit()
                db.refresh(admin)
                return admin
        except Exception as e:
            print(f"Error adding admin: {e}")
