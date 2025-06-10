import pytest
from app import create_app
from db import stores

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "PROPAGATE_EXCEPTIONS": True,  # Added this to help with debugging
    })
    # Other setup can go here...
    yield app
    # Clean up can go here...

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def clean_stores():
    stores.clear()
    yield
