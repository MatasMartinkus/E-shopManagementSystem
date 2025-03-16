import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.order import Order, OrderProduct
from src.models.customer import Customer
from src.models.product import Product
from src.models.warehouse import Warehouse
from src.utils.dbengine import Base
from datetime import datetime

class TestOrderModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_order(self):
        customer = Customer(name="John", last_name="Doe", phone="555-555-5555")
        self.session.add(customer)
        self.session.commit()

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

        order = Order(customer_id=customer.id, date_created=datetime.utcnow())
        self.session.add(order)
        self.session.commit()

        order_product = OrderProduct(
            order_id=order.id,
            product_id=product.id,
            name=product.name,
            price=product.price,
            quantity=2
        )
        self.session.add(order_product)
        self.session.commit()

        retrieved_order = self.session.query(Order).filter_by(customer_id=customer.id).first()
        self.assertIsNotNone(retrieved_order)
        self.assertEqual(len(retrieved_order.products), 1)

if __name__ == '__main__':
    unittest.main()