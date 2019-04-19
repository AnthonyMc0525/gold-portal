import sys
import os

from flask import Flask, render_template, request, flash, session
import psycopg2
import psycopg2.extras
from werkzeug.security import check_password_hash, generate_password_hash


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.urandom(24)

    from . import courses
    app.register_blueprint(courses.bp)
    app.add_url_rule('/', endpoint='index')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='portal',
        DB_USER='portal_user',
        EMAIL='teacher@stevenscollege.edu',
        PASSWORD=generate_password_hash('qwerty'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        logged_in = False
        method = request.method
        if method == 'POST':
            email = request.form['email']
            password = request.form['password']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
                    user = cur.fetchone()
                    
            if email is None:
                error = 'Incorrect email'
            elif not check_password_hash(user['password'], password):
                error = 'Your Password was Incorrect'
            print(error)

            if error is None:
                logged_in = True
                session.clear()
                session['user_id'] = user['first_name']


        return render_template('index.html', logged_in=logged_in,session=session)


    @app.route('/getsession')
    def get_session():
        if 'user_id' in session:
            return str(session['user_id'])
        else:
            return 'You are not logged in'


    return app
