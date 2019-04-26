from flask import g, session

def test_login(client, auth):
    # get the page
    with client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'<form method = "post">' in response.data

    with client:
        response = auth.login()
        assert response.status_code == 200
        assert b'<form method = "post">' not in response.data
        assert b'Logout' in response.data
        # assert b'1' in response.data




    
    # check session user_id for correct id
