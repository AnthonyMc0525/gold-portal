
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

def get_course(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM courses WHERE course_id=%s", (id,))
    course = cur.fetchone()
    cur.close()

    return course

def get_user(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    user = cur.fetchone()
    cur.close()

    return user

@bp.route('/')
@login_required
def index():
    user = get_user(id)

    con = get_db()
    cur = con.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()
    cur.close()

    return render_template('/courses/index.html', courses=courses, user=user)


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
        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO courses (name, number, description, teacher_id) VALUES (%s, %s, %s, %s)",
            (name, number, description, teacher_id)
        )
        con.commit()
        cur.close()

        flash('Success!')

    return render_template('/courses/create.html')


@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required 
def single(id):
    course = get_course(id)
    user = get_user(id)

    if request.method == 'get':
         name = request.form['name']
         number =  request.form['number']
         description = request.form['description']
         return redirect(url_for('courses.index'))

    return render_template('courses/single.html', course=course, user=user)



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
