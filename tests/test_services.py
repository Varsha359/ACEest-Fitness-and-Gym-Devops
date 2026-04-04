import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import services





def test_init_db(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    assert os.path.exists(services.DB_NAME)


def test_validate_user(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    role = services.validate_user("admin", "admin")
    assert role is not None


def test_invalid_user(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    role = services.validate_user("wrong", "wrong")
    assert role is None


def test_save_and_get_clients(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    services.save_client("Alice")
    clients = services.get_clients()

    assert "Alice" in clients


def test_save_client_empty(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    services.save_client("")
    clients = services.get_clients()

    assert clients == []


def test_save_progress(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    services.save_client("Bob")
    services.save_progress("Bob", 90)

    data = services.get_progress("Bob")
    assert len(data) == 1


def test_generate_chart_no_data(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    chart = services.generate_chart("NoUser")
    assert chart is None


def test_generate_chart_with_data(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    services.save_client("ChartUser")
    services.save_progress("ChartUser", 85)

    chart = services.generate_chart("ChartUser")
    assert chart is not None


def test_generate_pdf(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    file_path = services.generate_pdf("ReportUser")
    assert os.path.exists(file_path)


def test_generate_pdf_empty_name(tmp_path):
    services.DB_NAME = str(tmp_path / "test.db")
    services.init_db()

    file_path = services.generate_pdf("")
    assert os.path.exists(file_path)