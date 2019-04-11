import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from portal.db import get_db

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/create-course', methods=('GET', 'POST'))
def create_course():
    if request.method == "GET":
        return render_temaplate('create-course.html')

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

    return render_template('create-crouse.html', new_course=new_course)

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
