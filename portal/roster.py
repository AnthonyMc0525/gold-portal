import os
import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import login_required, teacher_required
from portal.db import get_db
from . import db

bp = Blueprint('roster', __name__)

def get_session(id):
    with db.get_db() as con:
        with con.cur() as cur:
            cur.execute('SELECT * FROM sessions WHERE session_id = %s', (id,))

# def get_course(id):
#     with db.get_db() as con:
#         with con.cur() as cur:
#             cur.execute('SELECT * FROM sessions WHERE session_id = %s', (id,))

@bp.route('/create-session/<int:course_id>', methods=['GET', 'POST'])
def create_session(course_id):
#    course = get_course(course_id)
    if request.method == 'POST':
        session_name = request.form['session_name']
        session_time_start = request.form['sessiontime_start']
        session_time_end = request.form['sessiontime_end']
        # a variable for all the students that are being added
        students = []
        session_id_list = []

        for key, value in request.form.items():
            students.append(value)
            
        students = set(students) - {session_name, session_time_start, session_time_end}

        with db.get_db() as con:
            with con.cur() as cur:
                cur.execute('INSERT INTO sessions (course_id, start_time, end_time) VALUES (%s, %s, %s,)', (course_id, session_time_start, session_time_end))

        with db.get_db() as con:
            with con.cur() as cur:
                cur.execute('SELECT session_id FROM session WHERE name=%s', (session_name,))
                session_id = cur.fetchone()

        with db.get_db() as con:
            with con.cur() as cur:
                for student in students:
                    student_id.append(cur.execute('SELECT session_id FROM users WHERE name=%s',() ).fetchone())

        with db.get_db() as con:
            with con.cur() as cur:
                for student in students:
                    cur.execute('INSERT INTO roster (session_id, user_id) VALUES (%s, %s, %s)', (session_id, student_id))

    
    return render_template('roster/create-roster.html')
# session_name=session['name'])
