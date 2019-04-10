import sys
import os

from flask import Flask, render_template, flash, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import courses
    app.register_blueprint(courses.bp)
    app.add_url_rule('/', endpoint='index')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='portal',
        DB_USER='portal_user',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    @app.route('/', methods=('GET', 'POST'))
    def index():
        method = request.method
        if method == 'POST':
            email = request.form['email']
            password = request.form['password']
            con = db.get_db()
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cur.fetchone()
            if user == None:
                flash('Your Email was Incorrect')
            elif user[2] != password:
                flash('Your Password was Incorrect')
            cur.close()
            con.close()
        return render_template('index.html', method=method)


    return app
