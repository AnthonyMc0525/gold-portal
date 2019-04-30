def test_assigments(client, auth):

    with client:
        auth.login()
        response = client.get('/assignments/create/1')
        assert response.status_code == 200
        assert b'Assignments' in response.data
        assert b'<form method = "post">' not in response.data


def test_assignment_create(client, auth):
    # get the page
    with client:
        response = auth.login()
        assert response.status_code == 200

        response = client.get('/assignments/create/1')
        assert response.status_code == 200
        assert b'<form method = "post">' not in response.data

        response = client.get('/assignments/create/1')
        assert response.status_code == 200
        assert b'form class="create-assignment"' in response.data
        assert b'Success!' not in response.data

        response = client.post('/assignments/create/1', data={
            'name': 'Test 1',
            'due_date': '2019-04-25',
            'description': 'Zach day',
            'course_id': '3'
        })
        assert response.status_code == 302
        
def test_assignment_update(client, auth):
    with client:
        response = auth.login()
        assert response.status_code == 200

        response = client.get('/assignments/create/1')
        assert response.status_code == 200
        assert b'form class="create-assignment"' in response.data
        assert b'Success!' not in response.data

        response = client.post('/assignments/create/1', data={
            'name': 'Test 1',
            'due_date': '2019-04-25',
            'description': 'Zach day',
            'course_id': '3'
        })

        response = client.get('/assignments/update/1')

        response = client.post('/assignments/update/1', data={
            'name': 'Test 1',
            'due_date': '2019-04-25',
            'description': 'Yes',
            'course_id': '3'
        })

def test_assignment(client, auth):
    response = client.get('/')
    assert b'<main class="course-list"' not in response.data

    with client:
        response = auth.login2()
        assert response.status_code == 200

        response = client.get('/assignments/create/1')
       # assert response.status_code == 200

        response = client.post('/assignments/create/1', data={
            'name': 'other thing',
            'due_date': '2018-02-02',
            'description': 'yes',
            'course_id': '2'
        })
        response = client.get('/assignments/')
        assert b'other thing' in response.data
        assert b'<form method = "post">' not in response.data

def test_assignment_single(client, auth):
    with client:
        response = auth.login()
        assert response.status_code == 200

        response = client.get('/courses/create')
        assert response.status_code == 200
        assert b'form class="create-course"' in response.data
        assert b'Success!' not in response.data

        response = client.post('/assignments/create/1', data={
            'name': 'other',
            'due_date': '2018-02-02',
            'description': 'yes',
            'course_id': '2'
        })

        response = client.get('/assignments/1')
        assert response.status_code == 200
        assert b'Success' in response.data
