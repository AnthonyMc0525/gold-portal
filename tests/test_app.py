from portal import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<form>' in response.data

def test_files_course_exist(client):
    response = client.get('/courses/')
    assert b'<h1>TSCT Portal</h1>' in response.data

    response = client.get('/courses/create')
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<form method="post">' in response.data

    response = client.get('/courses/update')
    assert b'<h2>Edit Course</h2>' in response.data

def test_create_course_post(client):
    def post_data(course = 'web dev II', course_id = 'CSET 160', course_description = 'This is web dev 2'):
            return client.post(
            '/courses/create',
            data={'course': course, 'course_id': course_id, 'course_description': course_description})

    response = post_data()
    assert b'<div' in response.data
    assert response.status_code == 200

def test_update_course_post(client):
    def post_data(course = 'web dev III', course_id = 'CSET 160', course_description = 'This is web dev 3'):
            return client.post(
            '/courses/update',
            data={'course': course, 'course_id': course_id, 'course_description': course_description})

    response = post_data()
    assert b'<div>' in response.data
    assert response.status_code == 200
    # see if post method works
