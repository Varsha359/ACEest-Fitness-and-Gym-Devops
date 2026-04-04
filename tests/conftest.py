import pytest
import os
import tempfile
from app import create_app
from app.services import init_db
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config["TESTING"] = True

    # Override DB
    from app import services
    services.DB_NAME = db_path

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)