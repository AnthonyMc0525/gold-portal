def test_course_list(client, auth):
    response = client.get('/courses/index')
    assert b'<main class="course-list"' not in response.data
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        response = auth.login()
        assert response.status_code == 200
        response = client.get('/courses/index')
        assert b'<main class="course-list"' in response.data
        assert b'<form method = "post">' not in response.data


def test_course_create(client, auth):
    # get the page
    with client:
        response = auth.login()
        assert response.status_code == 200

        response = client.get('/courses/index')
        assert response.status_code == 200
        assert b'CSET160' not in response.data

        response = client.get('/courses/create')
        assert response.status_code == 200
        assert b'form class="create-course"' in response.data
        assert b'Success!' not in response.data
        
        response = client.post('/courses/create', data={
            'name': 'Web Development II',
            'number': 'CSET160',
            'description': 'The best course ever.'
        })
        assert response.status_code == 200
        assert b'Success!' in response.data

        response = client.get('/courses/index')
        assert b'Web Development II' in response.data
        
        
