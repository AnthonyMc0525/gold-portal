from flask import g, session

def test_login(client, auth):
    # get the page
    response = client.get('/')
    assert response.status_code == 200
    assert b'<form method = "post">' in response.data

    with client:
        response = auth.login()
        assert response.status_code == 200
        assert b'<form method = "post">' not in response.data
        assert b'logout' in response.data
        # assert b'1' in response.data
        response = client.get('/')
        print(response.data)
        assert b'teacher' in response.data

def test_logout(client,auth):
    auth.login()

    with client:
        auth.logout()
        assert g.user not in session

    # check session user_id for correct id
