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
        name = request.form['session_name']
        session_time_start = request.form['sessiontime_start']
        session_time_end = request.form['sessiontime_end']


        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO sessions (name, session_time_start, session_time_end) VALUES (%s, %s, %s)", (name, session_time_start, session_time_end))
        cur.close()

    return render_template('/roster/create-session.html')
