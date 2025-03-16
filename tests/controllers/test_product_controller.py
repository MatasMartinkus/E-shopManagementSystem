import unittest
from unittest.mock import MagicMock, patch
from src.controllers.product_controller import ProductController

class TestProductController(unittest.TestCase):
    def setUp(self):
        self.product_controller = ProductController()

    @patch('src.controllers.product_controller.get_db')
    def test_add_product(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1, location="Location1", capacity=1000, max_volume=10000, max_weight=10000, current_volume=5000, current_weight=5000)
        
        self.product_controller.add_product(
            name="Product1",
            description="Description1",
            price=10.0,
            stock_quantity=10,
            category="Category1",
            subcategory="Subcategory1",
            length=1.0,
            width=1.0,
            height=1.0,
            weight=1.0,
            warehouse_id=1
        )
        
        mock_db.add.assert_called()
        mock_db.commit.assert_called()


    @patch('src.controllers.product_controller.get_db')
    def test_delete_product(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
        
        self.product_controller.delete_product(1)
        
        mock_db.delete.assert_called()
        mock_db.commit.assert_called()

    @patch('src.controllers.product_controller.get_db')
    def test_get_warehouse_products_by_warehouse_id(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.all.return_value = [MagicMock(id=1, name="Product1")]
        
        products = self.product_controller.get_warehouse_products_by_warehouse_id(1)
        
        self.assertEqual(len(products), 1)

if __name__ == '__main__':
    unittest.main()