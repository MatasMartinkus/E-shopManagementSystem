from src.utils.dbengine import get_db
from src.models.manager import Manager

class ManagerController:
    def add_manager(self, location, permissions, user_id):
        with get_db() as db:
            manager = Manager(location=location, permissions=permissions, user_id=user_id)
            db.add(manager)
            db.commit()
            db.refresh(manager)
            return manager
    
    def get_manager_by_user_id(self, user_id):
        with get_db() as db:
            return db.query(Manager).filter(Manager.user_id == user_id).first()