def test_assigments(client, auth):

    with client:
        auth.login()
        response = client.get('/assignments/create')
        assert response.status_code == 200
        assert b'Assignments' in response.data
        assert b'<form method = "post">' not in response.data


# def test_assignment_create(client, auth):
#     # get the page
#     with client:
#         response = auth.login()
#         assert response.status_code == 200
#
#         response = client.get('/courses/')
#         assert response.status_code == 200
#         assert b'CSET160' not in response.data
#
#         response = client.get('/courses/create')
#         assert response.status_code == 200
#         assert b'form class="create-course"' in response.data
#         assert b'Success!' not in response.data
#
#         response = client.post('/courses/create', data={
#             'name': 'Web development 2',
#             'number': 'CSET200',
#             'description': 'SKDMKD',
#         })
#         assert response.status_code == 200
#         assert b'Success!' in response.data
#
#
# def test_course_owner(client, auth):
#     with client:
#
#         response = client.get('/courses/')
#         assert b'Web development 2' not in response.data
#
#     with client:
#         response = auth.login()
#         assert response.status_code == 200
#
#         response = client.get('/courses/')
#         assert response.status_code == 200
#         assert b'Web development 2' in response.data
