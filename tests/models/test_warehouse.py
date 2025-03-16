import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.warehouse import Warehouse, WarehouseAdministrator, Item
from src.models.product import Product
from src.utils.dbengine import Base
from datetime import datetime

class TestWarehouseModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_warehouse(self):
        warehouse = Warehouse(
            location="Location1",
            capacity=1000,
            max_volume=10000,
            max_weight=10000,
            current_volume=5000,
            current_weight=5000
        )
        self.session.add(warehouse)
        self.session.commit()

        retrieved_warehouse = self.session.query(Warehouse).filter_by(location="Location1").first()
        self.assertIsNotNone(retrieved_warehouse)
        self.assertEqual(retrieved_warehouse.capacity, 1000)

    def test_create_warehouse_administrator(self):
        warehouse = Warehouse(location="Location1", capacity=1000)
        self.session.add(warehouse)
        self.session.commit()

        admin = WarehouseAdministrator(
            warehouse_id=warehouse.id,
            name="Admin1",
            last_name="Last1",
            dob=datetime(2000, 1, 1),
            hourly_rate=20.0,
            start_date=datetime(2022, 1, 1),
            end_date=datetime(2023, 1, 1),
            job_title="Manager"
        )
        self.session.add(admin)
        self.session.commit()

        retrieved_admin = self.session.query(WarehouseAdministrator).filter_by(name="Admin1").first()
        self.assertIsNotNone(retrieved_admin)
        self.assertEqual(retrieved_admin.last_name, "Last1")

    def test_create_item(self):
        warehouse = Warehouse(location="Location1", capacity=1000)
        self.session.add(warehouse)
        self.session.commit()

        product = Product(
            warehouse_id=warehouse.id,
            name="Product1",
            description="Description1",
            price=10.0,
            stock_quantity=100
        )
        self.session.add(product)
        self.session.commit()

        item = Item(
            product_id=product.id,
            quantity=10,
            warehouse_id=warehouse.id
        )
        self.session.add(item)
        self.session.commit()

        retrieved_item = self.session.query(Item).filter_by(product_id=product.id).first()
        self.assertIsNotNone(retrieved_item)
        self.assertEqual(retrieved_item.quantity, 10)

if __name__ == '__main__':
    unittest.main()