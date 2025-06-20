from base_test import BaseTest

class StoreTest(BaseTest):
    def test_get_store(self):
        """Test retrieving a store by ID"""
        # Create a test store first
        response = self.client.post('/store', json={"name": "Test Store"})
        store_id = response.get_json()["id"]

        # Test get store endpoint
        response = self.client.get(f'/store/{store_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Test Store")

    def test_get_store_not_found(self):
        """Test retrieving a store that does not exist"""
        response = self.client.get('/store/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_delete_store(self):
        """Test deleting a store by ID"""
        # Create a test store first
        response = self.client.post('/store', json={"name": "Test Store"})
        store_id = response.get_json()["id"]

        # Test delete endpoint
        response = self.client.delete(f'/store/{store_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Store deleted")

    def test_delete_store_not_found(self):
        """Test deleting a store that does not exist"""
        response = self.client.delete('/store/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_get_all_stores(self):
        """Test retrieving all stores"""
        # Create test stores
        self.client.post('/store', json={"name": "Store 1"})
        self.client.post('/store', json={"name": "Store 2"})

        response = self.client.get('/store')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_create_store(self):
        """Test creating a new store"""
        response = self.client.post('/store', json={"name": "New Store"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "New Store")

    def test_create_store_duplicate(self):
        """Test creating a store with a duplicate name"""
        # Create first store
        self.client.post('/store', json={"name": "New Store"})
        
        # Try to create duplicate
        response = self.client.post('/store', json={"name": "New Store"})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
