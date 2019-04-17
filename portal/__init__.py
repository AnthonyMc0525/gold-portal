import sys
import os
import functools

from flask import Flask, render_template, request, flash, session, g, redirect, url_for
import psycopg2
import psycopg2.extras

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view

def teacher_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user[5] != "teacher":
            return redirect(url_for("courses.index"))

        return view(**kwargs)

    return wrapped_view

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.urandom(24)

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

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            connection = db.get_db()
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE id = %s', (user_id,)
            )
            g.user = cursor.fetchone()


    from . import courses
    app.register_blueprint(courses.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        method = request.method
        if method == 'POST':
            email = request.form['email']
            password = request.form['password']
            con = db.get_db()
            cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
            error = None
            cur.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cur.fetchone()

            if user is None:
                error = 'Incorrect error'
            elif user['password'] != password:
                error = 'Your Password was Incorrect'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                g.user = user

            cur.close()
            con.close()

        return render_template('index.html')


    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))


    return app
