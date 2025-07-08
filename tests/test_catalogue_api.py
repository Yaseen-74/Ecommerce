import pytest
from flask_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_catalogue():
    return {
        "name": "Test Product",
        "description": "Test Description",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "active": True
    }

def test_create_catalogue(client, sample_catalogue):
    response = client.post("/api/catalogues", json=sample_catalogue)
    assert response.status_code in (200, 201)
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["name"] == sample_catalogue["name"]

def test_get_catalogue_by_id(client, sample_catalogue):
    create_res = client.post("/api/catalogues", json=sample_catalogue)
    assert create_res.status_code in (200, 201)
    created_id = create_res.get_json()["data"]["ID"]

    get_res = client.get(f"/api/catalogues/{created_id}")
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert data["status"] == "success"
    assert data["data"]["name"] == sample_catalogue["name"]
    assert data["data"].get("catalogue_id") == created_id  

def test_update_catalogue(client):
    
    create_res = client.post("/api/catalogues", json={
        "name": "UpdateMe",  
        "description": "Original Desc",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "active": True
    })
    assert create_res.status_code in (200, 201)
    catalogue_id = create_res.get_json()["data"]["ID"]

 
    update_data = {
        "name": "Updated",  
        "description": "Updated Desc",
        "start_date": "2025-02-01",
        "end_date": "2025-12-30",
        "active": False
    }

    update_res = client.put(f"/api/catalogues/{catalogue_id}", json=update_data)
    assert update_res.status_code == 200
    data = update_res.get_json()
    assert data["status"] == "success"
    assert data["message"] == "Catalogue updated successfully"



def test_get_all_catalogues(client):
    response = client.get("/api/catalogues")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)

def test_delete_and_check_not_found(client):
    res = client.post("/api/catalogues", json={
        "name": "ToDelete",
        "description": "Delete me",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "active": True
    })
    assert res.status_code in (200, 201)
    catalogue_id = res.get_json()["data"]["ID"]

    del_res = client.delete(f"/api/catalogues/{catalogue_id}")
    assert del_res.status_code == 200
    assert del_res.get_json()["message"] == "Catalogue deleted successfully"

    get_res = client.get(f"/api/catalogues/{catalogue_id}")
    assert get_res.status_code == 404
