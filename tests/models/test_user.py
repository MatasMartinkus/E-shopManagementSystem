import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.user import User
from src.utils.dbengine import Base

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_user(self):
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password",
            is_verified=True,
            role="customer"
        )
        self.session.add(user)
        self.session.commit()

        retrieved_user = self.session.query(User).filter_by(username="testuser").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, "test@example.com")
        self.assertTrue(retrieved_user.is_verified)

if __name__ == '__main__':
    unittest.main()