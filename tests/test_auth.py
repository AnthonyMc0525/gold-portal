def test_login(client, auth):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<form method = "post">' in response.data
    response = auth.login()
    assert response.status_code == 200
    assert b'<form method = "post">' not in response.data
    assert b'Logout' in response.data
