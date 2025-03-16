import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.customer import Customer
from src.models.user import User
from src.utils.dbengine import Base

class TestCustomerModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_customer(self):
        user = User(username="testuser", email="test@example.com", hashed_password="hashed_password")
        self.session.add(user)
        self.session.commit()

        customer = Customer(
            name="John",
            last_name="Doe",
            phone="555-555-5555",
            address="123 Main St",
            user_id=user.id
        )
        self.session.add(customer)
        self.session.commit()

        retrieved_customer = self.session.query(Customer).filter_by(name="John").first()
        self.assertIsNotNone(retrieved_customer)
        self.assertEqual(retrieved_customer.last_name, "Doe")
        self.assertEqual(retrieved_customer.phone, "555-555-5555")

if __name__ == '__main__':
    unittest.main()