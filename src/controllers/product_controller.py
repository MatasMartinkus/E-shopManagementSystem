from src.utils.dbengine import get_db
from src.models.product import Product
from src.models.warehouse import Warehouse

class ProductController:
    def add_product(self, name, description, price, stock_quantity, category=None, 
                    subcategory=None, length=None, width=None, height=None, weight=None, 
                    warehouse_id=None):
        
        # Check if there is enough space in the warehouse
        if not self.check_warehouse_space(weight, length, width, height, warehouse_id, stock_quantity):
            raise ValueError("Not enough space in the warehouse")
        else:
            with get_db() as db:
                # Check if a warehouse is provided
                if warehouse_id:
                    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
                    if not warehouse:
                        raise ValueError("Warehouse not found")
                else:
                    # Create a new warehouse if none is provided
                    warehouse = Warehouse(location="Default Location", capacity=1000)
                    db.add(warehouse)
                    db.commit()
                    db.refresh(warehouse)
                    warehouse_id = warehouse.id
                
                # Create the product
                product = Product(
                    name=name,
                    description=description,
                    price=price,
                    stock_quantity=stock_quantity,
                    category=category,
                    subcategory=subcategory,
                    length=length,
                    width=width,
                    height=height,
                    weight=weight,
                    warehouse_id=warehouse_id
                )
                db.add(product)

                warehouse.current_weight += weight * stock_quantity
                warehouse.current_volume += (length * width * height) * stock_quantity

                db.commit()
                db.refresh(product)
                return product

    def edit_product(self, product_id, name=None, description=None, price=None, stock_quantity=None, category=None, subcategory=None, 
                     length=None, width=None, height=None, weight=None, warehouse_id=None):
        
        with get_db() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return None
            else:
                if stock_quantity:
                    if not self.check_warehouse_space(weight, length, width, height,warehouse_id, stock_quantity):
                        raise ValueError("Not enough space in the warehouse")
                    else:
                        warehouse = db.query(Warehouse).filter(Warehouse.id == product.warehouse_id).first()
                        warehouse.current_weight -= product.weight * product.stock_quantity
                        warehouse.current_volume -= (product.length * product.width * product.height) * product.stock_quantity
                        
                        if name:
                            product.name = name
                        if description:
                            product.description = description
                        if price:
                            product.price = price
                        if stock_quantity:
                            product.stock_quantity = stock_quantity
                        if category:
                            product.category = category
                        if subcategory:
                            product.subcategory = subcategory
                        if length:
                            product.length = length
                        if width:
                            product.width = width
                        if height:
                            product.height = height
                        if weight:
                            product.weight = weight
                        if warehouse_id:
                            warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
                            if not warehouse:
                                raise ValueError("Warehouse not found")
                            product.warehouse_id = warehouse_id
                        db.commit()
                        db.refresh(product)
                        return product

    def get_all_products(self):
        with get_db() as db:
            return db.query(Product).all()
        
    def get_warehouse_products_by_warehouse_id(self, warehouse_id):
        with get_db() as db:
            return db.query(Product).filter(Product.warehouse_id == warehouse_id).all()

    def delete_product(self, product_id):
        with get_db() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                db.delete(product)
                db.commit()
    def get_warehouse_for_product(self, product_id):
        with get_db() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                warehouse = db.query(Warehouse).filter(Warehouse.id == product.warehouse_id).first()
                return warehouse
            return None
        
    def get_product_by_id(self, product_id):
        with get_db() as db:
            return db.query(Product).filter(Product.id == product_id).first()
        
    def search_products(self, search_term, filter_by):
        with get_db() as db:
            if filter_by == "Name":
                return db.query(Product).filter(Product.name.ilike(f"%{search_term}%")).all()
            elif filter_by == "Description":
                return db.query(Product).filter(Product.description.ilike(f"%{search_term}%")).all()
            elif filter_by == "Category":
                return db.query(Product).filter(Product.category.ilike(f"%{search_term}%")).all()
            elif filter_by == "Subcategory":
                return db.query(Product).filter(Product.subcategory.ilike(f"%{search_term}%")).all()
            else:
                return db.query(Product).filter(
                    (Product.name.ilike(f"%{search_term}%")) |
                    (Product.description.ilike(f"%{search_term}%")) |
                    (Product.category.ilike(f"%{search_term}%")) |
                    (Product.subcategory.ilike(f"%{search_term}%"))
                ).all()
    

    
    def check_warehouse_space(self, weight, length, width, height, warehouse_id, quantity):
        with get_db() as db:
            warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
            if not warehouse:
                raise ValueError("Warehouse not found")
            else:
                # Check if the warehouse has enough space
                if warehouse.current_weight + weight * quantity > warehouse.max_weight:
                    return False
                if warehouse.current_volume + (length * width * height) * quantity > warehouse.max_volume:
                    return False
                return True
        
        

        
