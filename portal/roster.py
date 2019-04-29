import os
import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import login_required, teacher_required
from portal.db import get_db

bp = Blueprint('roster', __name__)

@bp.route('/create-session', methods=['GET', 'POST'])
def create_session():
    if request.method == 'POST':
        course_name = request.form['course_name']
        session_name = request.form['session_name']
        session_time_start = request.form['sessiontime_start']
        session_time_end = request.form['sessiontime_end']

        with db.get_db() as con:
            with con.cur() as cur:
                course_id = cur.execute('SELECT course_id FROM courses WHERE name = %s', (course_name,)).fetchone()

        with db.get_db() as con:
            with con.cur() as cur:
                cur.execute('INSERT INTO sessions(course_id, start_time, end_time) VALUES (%s, %s, %s,)', (course_id, session_time_start, session_time_end))


    return render_template('/roster/create-session.html')
