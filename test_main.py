from fastapi.testclient import TestClient
from ..main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base
from ..auth import get_db
import pytest


TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    
    Base.metadata.create_all(bind=engine)
    yield
  
    Base.metadata.drop_all(bind=engine)

def get_test_token(username="testuser", password="testpass", role="user"):
    
    client.post("/users/", json={"username": username, "password": password, "role": role})
    
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_create_user(setup_db):
    response = client.post("/users/", json={"username": "testuser", "password": "testpass", "role": "user"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login(setup_db):
    client.post("/users/", json={"username": "admin", "password": "adminpass", "role": "admin"})
    response = client.post("/login", data={"username": "admin", "password": "adminpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_submit_ticket(setup_db):
    token = get_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tickets/", json={"description": "Test ticket"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["description"] == "Test ticket"

def test_unauthorized_update(setup_db):
    token = get_test_token()  
    headers = {"Authorization": f"Bearer {token}"}
    
    create_response = client.post("/tickets/", json={"description": "Ticket to update"}, headers=headers)
    ticket_id = create_response.json()["id"]
    
    update_response = client.put(f"/tickets/{ticket_id}", json={"status": "closed"}, headers=headers)
    assert update_response.status_code == 403  

def test_create_asset(setup_db):
    token = get_test_token(username="admin", password="adminpass", role="admin") 
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/assets/", json={"name": "Laptop", "location": "Office"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_get_stats(setup_db):
    token = get_test_token(username="admin", password="adminpass", role="admin")  
    headers = {"Authorization": f"Bearer {token}"}
    
    user_token = get_test_token()
    user_headers = {"Authorization": f"Bearer {user_token}"}
    client.post("/tickets/", json={"description": "Test1"}, headers=user_headers)
    client.post("/tickets/", json={"description": "Test2"}, headers=user_headers)
    response = client.get("/stats/", headers=headers)
    assert response.status_code == 200
    assert "avg_resolution_time" in response.json()

if __name__ == "__main__":
    pytest.main([__file__])