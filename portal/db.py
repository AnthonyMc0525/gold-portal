import os
import psycopg2
from psycopg2.extras import DictCursor


import click
from flask import current_app, g
from flask.cli import with_appcontext
from sys import argv
from werkzeug.security import generate_password_hash

def get_db():
    if 'db' not in g:
        # open a connection, save it to close when done
        DB_URL = os.environ.get('DATABASE_URL', None)
        if DB_URL:
            g.db = psycopg2.connect(DB_URL, sslmode='require', cursor_factory=DictCursor)
        else:
            g.db = psycopg2.connect(

                dbname=current_app.config['DB_NAME'], 
                user=current_app.config['DB_USER'],
                cursor_factory=DictCursor 
            )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close() # close the connection


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        with db.cursor() as cur:
            cur.execute(f.read())
            db.commit()

def create_user():
    con = get_db()
    print("Enter user's First Name")
    first_name = input(">")
    print("Enter user's Last Name")
    last_name = input(">")
    print("Enter user's Email")
    email = input(">")
    print("Enter user's Password")
    password = input(">")
    print("Enter user's Role")
    role = input(">")
    with get_db() as con:
        with con.cursor() as cur:
            cur.execute(
                "INSERT INTO users(first_name, last_name,  email, password, role) VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, email, generate_password_hash(password), role)
            )
            con.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('create-user')
@with_appcontext
def create_user_command():
    create_user()
    click.echo('Created user')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_user_command)
