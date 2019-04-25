def test_assignment(client, auth):
    response = client.get('/')
    assert b'<main class="course-list"' not in response.data

    with client:
        response = auth.login2()
        assert response.status_code == 200
        response = client.get('/')
        assert b'other thing' in response.data
        assert b'<form method = "post">' not in response.data
