def test_create_account(client):
    response = client.post(
        "/api/v1/accounts/",
        json={"username": "toto", "email": "toto@gmail.com", "password": "123456", "type": "user"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "toto"
    assert response.json()["email"] == "toto@gmail.com"


def test_read_account(client):
    response = client.get("/api/v1/accounts/")
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"
