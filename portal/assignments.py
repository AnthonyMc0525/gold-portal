import os
import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import DictCursor

from . import login_required, teacher_required
from portal.db import get_db
from portal.courses import get_course

bp = Blueprint('assignments', __name__, url_prefix='/assignments')


@bp.route('/list/<int:id>')
@login_required
def index(id):
    course = get_course(id)
    user = get_user(id)
    con = get_db()
    cur = con.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM assignments WHERE course_id = %s", (id,))
    assignments = cur.fetchall()
    cur.close()

    return render_template('/assignments/index.html', assignments=assignments, user=user, course=course)


@bp.route('/create/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def create(id):
    course = get_course(id)

    if request.method == 'POST':
        name = request.form['name']
        due_date = request.form['due_date']
        description = request.form['description']

        if name == '' or due_date == '' or description == '':
            return redirect(url_for('assignments.index'))

        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO assignments (name, due_date, description, course_id) VALUES (%s, %s, %s, %s)", (name, due_date, description, id))
        con.commit()
        cur.close()

        flash('Success!')
        return redirect(url_for('courses.index'))

    return render_template('assignments/create.html', course=course)

def get_assignment(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM assignments WHERE id=%s", (id,))
    assignments = cur.fetchone()
    cur.close()

    return assignments

def get_user(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cur.fetchone()
    cur.close()

    return user

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def update(id):
    assignments = get_assignment(id)
    if request.method == 'POST':
         name = request.form['name']
         due_date =  request.form['due_date']
         description = request.form['description']

         if name == '' or due_date == '' or description == '':
             return redirect(url_for('index'))

         con = get_db()
         cur = con.cursor()
         cur.execute("UPDATE assignments SET name = %s, due_date = %s, description = %s WHERE id = %s", (name, due_date, description, id,))
         con.commit()
         cur.close()

         return redirect(url_for('index'))

    return render_template('assignments/update.html', assignments=assignments)



@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def single(id):
    assignments = get_assignment(id)
    user = get_user(id)

    if request.method == 'get':
         name = request.form['name']
         due_date =  request.form['due_date']
         description = request.form['description']

         return redirect(url_for('courses.index'))

    return render_template('assignments/single.html', user=user, assignments=assignments)
