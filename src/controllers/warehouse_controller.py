from src.utils.dbengine import get_db
from src.models.warehouse import Warehouse, WarehouseAdministrator, Item

class WarehouseController:
    LOCATIONS = ["Vilnius", "Kaunas", "Palanga", "Klaipėda", "Šiauliai", "Panevėžys", "Alytus", "Marijampolė", "Mažeikiai", "Jonava", "Utena", "Kėdainiai", "Telšiai", "Visaginas", "Tauragė", "Ukmergė", "Plungė", "Kretinga", "Šilutė", "Radviliškis", "Druskininkai", "Nida", "Birštonas", "Anykščiai", "Trakai", "Zarasai", "Švenčionys", "Šalčininkai", "Širvintos"]
    def add_warehouse(self, location, capacity, max_volume=None, max_weight=None, current_volume=0, current_weight=0):
        with get_db() as db:
            warehouse = Warehouse(location=location, capacity=capacity, max_volume=max_volume, max_weight=max_weight, current_volume=0, current_weight=0)
            db.add(warehouse)
            db.commit()
            db.refresh(warehouse)
            return warehouse

    def edit_warehouse(self, warehouse_id, location=None, capacity=None, max_volume=None, max_weight=None, current_volume=None, current_weight=None):
        with get_db() as db:
            warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
            if not warehouse:
                return None
            if location:
                warehouse.location = location
            if capacity:
                warehouse.capacity = capacity
            if max_volume:
                warehouse.max_volume = max_volume
            if max_weight:
                warehouse.max_weight = max_weight
            if current_volume:
                warehouse.current_volume = current_volume
            if current_weight:
                warehouse.current_weight = current_weight
            db.commit()
            db.refresh(warehouse)
            return warehouse

    def get_all_warehouses(self):
        with get_db() as db:
            return db.query(Warehouse).all()

    def delete_warehouse(self, warehouse_id):
        with get_db() as db:
            warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
            if warehouse:
                db.query(WarehouseAdministrator).filter(WarehouseAdministrator.warehouse_id == warehouse_id).delete()
                db.delete(warehouse)
                db.commit()

    def add_administrator(self, warehouse_id, name, last_name, dob, hourly_rate, start_date, end_date=None, job_title=None):
        with get_db() as db:
            warehouse_admin = WarehouseAdministrator(warehouse_id=warehouse_id, name=name, last_name=last_name, dob=dob, hourly_rate=hourly_rate, start_date=start_date, end_date=end_date, job_title=job_title)
            db.add(warehouse_admin)
            db.commit()
            db.refresh(warehouse_admin)
            return warehouse_admin
        
    def get_all_locations(self):
        return self.LOCATIONS
        
    def search_warehouses(self, search_term, filter_by):
        with get_db() as db:
            if filter_by == "Location":
                return db.query(Warehouse).filter(Warehouse.location.ilike(f"%{search_term}%")).all()
            elif filter_by == "Capacity":
                return db.query(Warehouse).filter(Warehouse.capacity == search_term).all()
            elif filter_by == "Max Volume":
                return db.query(Warehouse).filter(Warehouse.max_volume == search_term).all()
            elif filter_by == "Max Weight":
                return db.query(Warehouse).filter(Warehouse.max_weight == search_term).all()
            return db.query(Warehouse).all()
        
    def get_all_administrators(self):
        with get_db() as db:
            return db.query(WarehouseAdministrator).all()
        
    def get_administrator_by_id(self, admin_id):
        with get_db() as db:
            return db.query(WarehouseAdministrator).filter(WarehouseAdministrator.id == admin_id).first()
        
    def calculate_salary(self, hourly_rate, normal_hours, overtime_hours, holiday_hours):
        return hourly_rate * (normal_hours + 1.5 * overtime_hours + 2 * holiday_hours)
    


        
        