import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.manager import Manager
from src.models.user import User
from src.utils.dbengine import Base

class TestManagerModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_manager(self):
        user = User(username="testuser", email="test@example.com", hashed_password="hashed_password")
        self.session.add(user)
        self.session.commit()

        manager = Manager(user_id=user.id, location="Location1", permissions="all")
        self.session.add(manager)
        self.session.commit()

        retrieved_manager = self.session.query(Manager).filter_by(user_id=user.id).first()
        self.assertIsNotNone(retrieved_manager)
        self.assertEqual(retrieved_manager.location, "Location1")
        self.assertEqual(retrieved_manager.permissions, "all")

if __name__ == '__main__':
    unittest.main()