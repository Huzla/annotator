# Simple test to make sure the application starts up.

def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello"