from flask import Flask, render_template, request, redirect, session, flash, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

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

    @app.route('/', methods=('GET', 'POST'))
    def index():
        logged_in = False
        method = request.method
        print(method)
        if method == 'POST':
            email = request.form['email']
            password = request.form['password']
            con = db.get_db()
            cur = con.cursor()
            error = None
            cur.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cur.fetchone()
            if user is None:
                error = 'Incorrect error'
            elif user[4] != password:
                error = 'Your Password was Incorrect'
                
            if error is None:
                logged_in = True
                session.clear()
                session['user_id'] = user[0]

            cur.close()
            con.close()

        return render_template('index.html', logged_in=logged_in)


    return app
