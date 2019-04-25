from flask import session

def test_login(client, auth):
    # get the page
    response = client.get('/')
    assert response.status_code == 200
    assert b'<form method = "post">' in response.data
    response = auth.login()
    assert response.status_code == 200
    assert b'<form method = "post">' not in response.data
    assert b'logout' in response.data
    assert b'teacher' in response.data

def test_logout(client, auth):

    with client:
        auth.login()
        assert 'user_id' in session
        auth.logout()
        assert 'user_id' not in session
# logout test
# It is the opposite of login
# check if the session is gone after you hit the logout button
