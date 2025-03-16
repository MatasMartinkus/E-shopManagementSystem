import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.product import Product
from src.models.warehouse import Warehouse
from src.utils.dbengine import Base

class TestProductModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_product(self):
        warehouse = Warehouse(location="Location1", capacity=1000)
        self.session.add(warehouse)
        self.session.commit()

        product = Product(
            warehouse_id=warehouse.id,
            name="Product1",
            description="Description1",
            price=10.0,
            stock_quantity=100,
            category="Category1",
            subcategory="Subcategory1",
            length=1.0,
            width=1.0,
            height=1.0,
            weight=1.0
        )
        self.session.add(product)
        self.session.commit()

        retrieved_product = self.session.query(Product).filter_by(name="Product1").first()
        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product.description, "Description1")
        self.assertEqual(retrieved_product.price, 10.0)

if __name__ == '__main__':
    unittest.main()