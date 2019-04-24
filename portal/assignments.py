import os
import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import DictCursor

from . import login_required, teacher_required
from portal.db import get_db

bp = Blueprint('assignments', __name__, url_prefix='/assignments')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def assignment_create():
    if request.method == "POST":
        name = request.form['name']
        due_date = request.form['due_date']
        description = request.form['description']
        teacher_id = g.user[0]
        error = None

        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO assignments (name, due_date, description) VALUES (%s, %s, %s, %s)", (name, due_date, description))

        con.commit()
        cur.close()

        flash('Success!')

    return render_template('assignments/create.html')
