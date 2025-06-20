import unittest
from tests.base_test import BaseTest
from models.item import ItemModel
from db import db
import json

class TestItem(BaseTest):
    def test_get_item_list_empty(self):
        """Test retrieving an empty list of items"""        
        response = self.client.get("/item")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_item_list_with_items(self):
        """Test retrieving a list of items"""
        item = ItemModel(name="Test Item", price=10.99, store_id=1)
        item2 = ItemModel(name="Test Item 2", price=10.99, store_id=1)
        with self.app.app_context():
            db.session.add(item)
            db.session.add(item2)
            db.session.commit()

        response = self.client.get("/item")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 2)

    def test_create_item(self):
        """Test creating an item successfully"""
        test_data = {"name": "Test Item", "price": 10.99, "store_id": 1}
        response = self.client.post(
            "/item",
            data=json.dumps(test_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)["name"], "Test Item")
        self.assertEqual(json.loads(response.data)["price"], 10.99)
        self.assertIsNotNone(response.json["id"])

    def test_create_item_invalid_data(self):
        """Test creating an item with invalid data"""
        test_data = {"name": "Test Item"}
        response = self.client.post(
            "/item",
            data=json.dumps(test_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)

    def test_get_single_item(self):
        """Test retrieving a single item by ID"""
        item = ItemModel(name="Test Item", price=10.99, store_id=1)
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()
            item_id = item.id

        response = self.client.get(f"/item/{item_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["name"], "Test Item")

    def test_get_item_not_found(self):
        """Test retrieving a non-existent item"""
        response = self.client.get("/item/999")
        self.assertEqual(response.status_code, 404)

    def test_update_item(self):
        """Test updating an existing item"""
        item = ItemModel(name="Test Item", price=10.99, store_id=1)
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()
            item_id = item.id

        update_data = {"name": "Updated Item", "price": 15.99}
        response = self.client.put(
            f"/item/{item_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["name"], "Updated Item")
        self.assertEqual(json.loads(response.data)["price"], 15.99)

    def test_update_item_with_invalid_data(self):
        """Test updating an existing item with invalid data"""
        item = ItemModel(name="Test Item", price=10.99, store_id=1)
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()
            item_id = item.id

        update_data = {"name": "Updated Item", "price": 15.99, "bad_value": None}
        response = self.client.put(
            f"/item/{item_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        
    def test_update_item_create_new(self):
        """Test PUT creating new item if doesn't exist"""
        update_data = {"name": "New Item", "price": 15.99, "store_id": 1}
        response = self.client.put(
            "/item/999",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["name"], "New Item")
        self.assertEqual(json.loads(response.data)["id"], 999)

    def test_delete_item(self):
        """Test deleting an item"""
        item = ItemModel(name="Test Item", price=10.99, store_id=1)
        with self.app.app_context():
            db.session.add(item)
            db.session.commit()
            item_id = item.id

        response = self.client.delete(f"/item/{item_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "Item deleted."})

    def test_delete_item_not_found(self):
        """Test deleting a non-existent item"""
        response = self.client.delete("/item/999")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
