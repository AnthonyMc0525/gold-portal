from portal import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert b'Thaddeus Stevens' in response.data
    assert b'<form method = "post">' in response.data




