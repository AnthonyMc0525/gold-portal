import os

import pytest

from portal import create_app
from portal.db import get_db, init_db
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DB_NAME': 'portal_test',
        'DB_USER': 'portal_user',
        'EMAIL': 'teacher@stevenscollege.edu',
        'PASSWORD': 'qwerty',
    })

    with app.app_context():
        init_db()

        with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
            con = get_db()
            cur = con.cursor()
            cur.execute(f.read())
            cur.close()
            con.commit()
            con.close()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='teacher@stevenscollege.edu', password='qwerty'):
        return self._client.post(
            '/',
            data={'email': email, 'password': password}
        )

    #def create_course(self, course='CSET180', course_id='CSET180', course_description='This is 180'):
    #    return self._client.post(
    #        '/courses/create',
    #        data={'course': course, 'course_id': course_id, 'course_description': course_description}
    #    )

    def logout(self):
        return self._client.get('/')


@pytest.fixture
def auth(client):
    return AuthActions(client)
