import unittest
from app import create_app
from db import stores

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update({
            "TESTING": True,
            "PROPAGATE_EXCEPTIONS": True,
        })
        self.client = self.app.test_client()
        stores.clear()

    def tearDown(self):
        stores.clear()

if __name__ == '__main__':
    unittest.main()
