import os
import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import DictCursor

from . import login_required, teacher_required
from portal.db import get_db

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/')
@login_required
def index():
    con = get_db()
    cur = con.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()
    cur.close()

    return render_template('/courses/index.html', courses=courses)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create():
    if request.method == "POST":
        name = request.form['name']
        number = request.form['number']
        description = request.form['description']
        error = None

        # Save to database
        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO courses (name, number, description) VALUES (%s, %s, %s)",
            (name, number, description)
        )
        con.commit()
        cur.close()

        flash('Success!')

    return render_template('/courses/create.html')


@bp.route('/update', methods=['GET', 'POST'])
@login_required
@teacher_required
def update():
    if request.method == "GET":
        return render_template('/courses/update.html')

    elif request.method == "POST":
        course = request.form['course']
        course_id = request.form['course_id']
        course_description = request.form['course_description']
        error = None

        if course:

            # Save to database
            con = get_db()
            cur = con.cursor()
            cur.execute(
                    "SELECT * FROM courses WHERE course_id = %s",
                    (course_id,)
            )
            result=cur.fetchone()
            if result != None:
                cur.execute(
                        "UPDATE courses SET course = %s, course_description = %s WHERE course_id = %s",
                        (course, course_description, course_id)
                )
                flash('Success!', 'success')
                flash('Your new course is edited!', 'success')

            elif result == None:
                flash('That course does not exist')

            con.commit()
            con.close()

        return render_template('/courses/update.html', course=course)
    return render_template('/courses/update.html', course=course)
