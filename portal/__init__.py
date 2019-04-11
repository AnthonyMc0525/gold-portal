import sys
import os

from flask import Flask, render_template, flash, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

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


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/create-course', methods=['GET', 'POST'])
    def course():
        if request.method == "GET":
            return render_template('create-course.html')

        elif request.method == "POST":
            new_course = request.form['']

            if new_course:

                # Save to database
                con = db.get_db()
                cur = con.cursor()
                cur.execute(
                        "INSERT INTO courses (course, course_id, teacher) VALUES (%s, %s, %s)",
                        (new_course, course_id, teacher)
                )
                con.commit()
                cur.close()

                flash('Your new course is now created. Want to add another?', 'success')
            else:
                flash('You need to add some information first.', 'error')

        return render_template('create-course.html', new_course=new_course)

    return app
