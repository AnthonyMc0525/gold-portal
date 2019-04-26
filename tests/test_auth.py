from flask import session

def test_login(client, auth):
  
    with client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'<form method = "post">' in response.data

    with client:
        response = auth.login()
        assert response.status_code == 200
        assert b'<form method = "post">' not in response.data
        assert b'Logout' in response.data

def test_logout(client, auth):

    with client:
        auth.login()
        assert 'user_id' in session
        auth.logout()
        assert 'user_id' not in session