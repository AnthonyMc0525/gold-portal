def test_course_list(client, auth):
    response = client.get('/courses/')
    assert b'<main class="course-list"' not in response.data
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        response = auth.login()
        assert response.status_code == 200
        response = client.get('/courses/')
        assert b'<h2 class="course-list"' in response.data
        assert b'<form method = "post">' not in response.data


def test_course_create(client, auth):
    # get the page
    with client:
        response = auth.login()
        assert response.status_code == 200

        response = client.get('/courses/')
        assert response.status_code == 200
        assert b'CSET160' not in response.data

        response = client.get('/courses/create')
        assert response.status_code == 200
        assert b'form class="create-course"' in response.data
        assert b'Success!' not in response.data
        
        response = client.post('/courses/create', data={
            'name': 'Web development 2',
            'number': 'CSET200',
            'description': 'SKDMKD',
        })
        assert response.status_code == 200
        assert b'Success!' in response.data


def test_course_owner(client, auth):
    with client:

        response = client.get('/courses/')
        assert b'Web development 2' not in response.data

    with client:
        response = auth.login()
        assert response.status_code == 200
        
        response = client.get('/courses/')
        assert response.status_code == 200
        assert b'Web development 2' in response.data


def test_course_update(client, auth):
    with client:
        response = auth.login()
        assert response.status_code == 200
        
        response = client.get('/courses/create')
        assert response.status_code == 200
        assert b'form class="create-course"' in response.data
        assert b'Success!' not in response.data
        
        response = client.post('/courses/create', data={
            'name': 'Web development 2',
            'number': 'CSET200',
            'description': 'SKDMKD',
        })

        response = client.get('/courses/1/update')
        
        response = client.post('/courses/1/update', data={
            'name': 'Web development 2',
            'number': 'updated',
            'description': 'updated',
        })

