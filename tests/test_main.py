import os, pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app, db

@pytest.fixture
def client():
    client = app.test_client()
    cleanup()
    db.create_all()
    yield client

def cleanup():
    db.drop_all()


def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Introduz o teu nome' in response.data

def test_index_logged_in(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)
    response = client.get('/')
    assert b'Chat website' in response.data

def test_index_logout(client):
    client.get('/logout')
    test_index_not_logged_in(client)

def test_index_send_message(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)
    client.post('/add-message', data={"mensagem": "Teste!"}, follow_redirects=True)
    response = client.get('/')
    assert b'Teste!' in response.data
    assert b'Test User' in response.data