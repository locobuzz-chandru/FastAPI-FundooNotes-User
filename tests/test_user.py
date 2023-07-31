import json


def test_register_successfully(client, user_data):
    response = client.post("/user/register", content=json.dumps(user_data))
    assert response.status_code == 201


def test_verify_token_successfully(client, user_data):
    response = client.post("/user/register", content=json.dumps(user_data))
    token = response.json()["token"]
    response = client.get(f"/user/verify_token/{token}")
    assert response.status_code == 200


def test_verify_token_unsuccessfully(client, user_data):
    response = client.post("/user/register", content=json.dumps(user_data))
    token = response.json()["token"]
    response = client.get(f"/user/verify_token/{token}a")
    assert response.status_code == 400


def test_login_successfully(client, user_data):
    response = client.post("/user/register", content=json.dumps(user_data))
    token = response.json()["token"]
    client.get(f"/user/verify_token/{token}")
    response = client.post("/user/login", content=json.dumps({"username": "user", "password": "user"}))
    assert response.status_code == 200


def test_login_unsuccessfully(client, user_data):
    response = client.post("/user/register", content=json.dumps(user_data))
    token = response.json()["token"]
    client.get(f"/user/verify_token/{token}")
    response = client.post("/user/login", content=json.dumps({"username": "user_1", "password": "user_"}))
    assert response.status_code == 400


def test_authenticate_user_successfully(client, user_data):
    response = client.post("/user/register", content=json.dumps(user_data))
    token = response.json()["token"]
    client.get(f"/user/verify_token/{token}")
    response = client.post("/user/login", content=json.dumps({"username": "user", "password": "user"}))
    token = response.json()["access_token"]
    response = client.get(f"/user/authenticate_user/{token}")
    assert response.status_code == 200


def test_retrieve_user_successfully(client, user_data):
    response = client.post("/user/register", content=json.dumps(user_data))
    token = response.json()["token"]
    client.get(f"/user/verify_token/{token}")
    response = client.post("/user/login", content=json.dumps({"username": "user", "password": "user"}))
    token = response.json()["access_token"]
    response = client.get(f"/user/authenticate_user/{token}")
    user_id = response.json()
    response = client.get(f"/user/retrieve_user/{user_id}")
    assert response.status_code == 200
