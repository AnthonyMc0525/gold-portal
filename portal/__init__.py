import sys
import os
import functools

from flask import Flask, render_template, request, flash, session, g, redirect, url_for
import psycopg2
import psycopg2.extras
from werkzeug.security import check_password_hash, generate_password_hash

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
        PASSWORD=generate_password_hash('qwerty'),
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

#    def handle_500_error(e):
#        return '''
#       <body> 
#
#            <h1 style="display: inline-block;
#            font-size: 4em; position: relative;
#            left: 34vw;">Something went wrong</h1>
#
#           <p style="position: relative; left: 31vw;
#           font-size: 1.5em;"></p> 
#
#        </body>
#
#        ''', 500
#
#    app.register_error_handler(500, handle_500_error)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        method = request.method

        if method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = None
            error = None

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
                    user = cur.fetchone()


            if user is None:
                error = 'Incorrect email.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))

            flash(error)

        return render_template('index.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))


    return app
