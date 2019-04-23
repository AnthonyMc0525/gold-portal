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
    cur.execute("SELECT * FROM courses WHERE teacher_id = %s", (g.user['id'],))
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
        teacher_id = g.user[0]
        error = None


        # Save to database
        if course:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("INSERT INTO courses (course, course_id, course_description) VALUES (%s, %s, %s)",(course, course_id, course_description))

        flash('Success!')

    return render_template('/courses/create.html')

def get_course(id):
    
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM courses WHERE course_id=%s", (id,))
    

        if course:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("INSERT INTO courses (course, course_id, course_description) VALUES (%s, %s, %s)",(course, course_id, course_description))

        flash('Success!', 'success')
        flash('Your new course is created!', 'success')

    return course

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
@teacher_required
def update(id):
    course = get_course(id)
    if request.method == 'POST':
         name = request.form['name']
         number =  request.form['number']
         description = request.form['description']

         con = get_db()
         cur = con.cursor()
         cur.execute("UPDATE courses SET name = %s, number = %s, description = %s  WHERE course_id = %s", (name, number, description, id,))
         con.commit()

         return redirect(url_for('courses.index'))

    return render_template('courses/update.html', course=course)

