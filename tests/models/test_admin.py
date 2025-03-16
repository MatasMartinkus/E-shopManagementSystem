import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.admin import Admin
from src.models.user import User
from src.utils.dbengine import Base

class TestAdminModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_admin(self):
        user = User(username="testuser", email="test@example.com", hashed_password="hashed_password")
        self.session.add(user)
        self.session.commit()

        admin = Admin(user_id=user.id, department="IT", permissions="all")
        self.session.add(admin)
        self.session.commit()

        retrieved_admin = self.session.query(Admin).filter_by(user_id=user.id).first()
        self.assertIsNotNone(retrieved_admin)
        self.assertEqual(retrieved_admin.department, "IT")
        self.assertEqual(retrieved_admin.permissions, "all")

if __name__ == '__main__':
    unittest.main()