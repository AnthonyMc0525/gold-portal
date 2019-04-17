import sys
import os

from flask import Flask, render_template, request, flash, session, redirect, url_for
import psycopg2
import psycopg2.extras


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
        PASSWORD='qwerty',
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
            con = db.get_db()
            cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
            error = None
            cur.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cur.fetchone()
            print(user)
            if user is None:
                error = 'Incorrect error'
            elif user['password'] != password:
                error = 'Your Password was Incorrect'

            if error is None:
                logged_in = True
                session.clear()
                session['user_id'] = user['first_name']

            cur.close()
            con.close()

        return render_template('index.html', logged_in=logged_in,session=session)


    @app.route('/logout', methods=['GET'])
    def logout():
        session.clear()
        print('Got Here')
        return redirect(url_for('index'))

    return app
