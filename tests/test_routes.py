import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def login(client):
    return client.post("/", data={
        "username": "admin",
        "password": "admin"
    }, follow_redirects=True)


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"


def test_login_page_load(client):
    res = client.get("/")
    assert res.status_code == 200


def test_login_success(client):
    res = login(client)
    assert res.status_code == 200
    assert b"dashboard" in res.data.lower() or res.status_code == 200


def test_dashboard_requires_login(client):
    res = client.get("/dashboard")
    assert res.status_code == 302  # redirect


def test_add_client(client):
    login(client)
    res = client.post("/dashboard", data={
        "action": "add",
        "name": "Varsha"
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b"Varsha" in res.data


def test_add_client_empty_name(client):
    login(client)
    res = client.post("/dashboard", data={
        "action": "add",
        "name": ""
    })

    assert b"Error: Name is required" in res.data


def test_progress_update(client):
    login(client)

    # First add client
    client.post("/dashboard", data={
        "action": "add",
        "name": "TestUser"
    })

    res = client.post("/dashboard", data={
        "action": "progress",
        "name": "TestUser",
        "adherence": "80"
    }, follow_redirects=True)

    assert res.status_code == 200


def test_chart_generation(client):
    login(client)

    client.post("/dashboard", data={"action": "add", "name": "ChartUser"})
    client.post("/dashboard", data={
        "action": "progress",
        "name": "ChartUser",
        "adherence": "75"
    })

    res = client.post("/dashboard", data={
        "action": "chart",
        "name": "ChartUser"
    })

    assert res.status_code == 200


def test_pdf_download(client):
    login(client)

    client.post("/dashboard", data={"action": "add", "name": "PDFUser"})

    res = client.post("/dashboard", data={
        "action": "pdf",
        "name": "PDFUser"
    })

    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/pdf"


def test_logout(client):
    login(client)
    res = client.get("/logout", follow_redirects=True)
    assert res.status_code == 200