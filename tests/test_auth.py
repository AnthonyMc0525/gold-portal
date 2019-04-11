def test_login(client, auth):
    # get the page
    response = client.get('/')
    assert response.status_code == 200
    assert b'<form method = "post">' in response.data
    response = auth.login()
    assert response.status_code == 200
    assert b'<form method = "post">' not in response.data
    assert b'logout' in response.data
    # assert session['user.id'] == user[0]

    

    # check session user_id for correct id
    
