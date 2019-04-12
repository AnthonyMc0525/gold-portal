import functools

import os

import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

from portal.db import get_db

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/')
def index():
    db = get_db()
    #posts = db.execute(
    #    'SELECT p.id, title, body, created, author_id, username'
    #    ' FROM post p JOIN user u ON p.author_id = u.id'
    #    ' ORDER BY created DESC'
    #).fetchall()
    return render_template('/courses/index.html')

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('/courses/create.html')

    elif request.method == "POST":
        course = request.form.get('course', False)
        course_id = request.form['course_id']
        course_description = request.form['course_description']
        error = None

        if course:

            # Save to database
            con = db.get_db()
            cur = con.cursor()
            cur.execute(
                    "INSERT INTO courses (course, course_id, course_description) VALUES (%s, %s, %s)",

                    (course, course_id, course_description)

            )
            con.commit()
            con.close()
        flash('Success!', 'success')
        flash('Your new course is created!', 'success')

        return render_template('/courses/create.html', course=course)
    return render_template('/courses/create.html', course=course)
