import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.financial import Financial
from src.utils.dbengine import Base
from datetime import datetime

class TestFinancialModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_financial(self):
        financial = Financial(
            transaction_date=datetime.utcnow(),
            amount=100.0,
            transaction_type="income",
            recipient="Recipient",
            sender="Sender"
        )
        self.session.add(financial)
        self.session.commit()

        retrieved_financial = self.session.query(Financial).filter_by(amount=100.0).first()
        self.assertIsNotNone(retrieved_financial)
        self.assertEqual(retrieved_financial.transaction_type, "income")
        self.assertEqual(retrieved_financial.recipient, "Recipient")
        self.assertEqual(retrieved_financial.sender, "Sender")

if __name__ == '__main__':
    unittest.main()