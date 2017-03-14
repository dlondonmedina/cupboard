# -*- coding: utf-8 -*-
"""
    Cupboard
    ~~~~~~

    A recipe and food inventory application written to run as a local
    server or on an internet facing server using Flask and sqlite3

    :copywrite: (c) 2017 by Dylan Medina.
    :license: BSD, see LICENSE for more details.
"""

import os
import ConfigParser
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# Get configuration file
config = ConfigParser.RawConfigParser()
config.read('cupboard.cfg')

# create our application first
app = Flask(__name__, instance_path=config.get("app_config", "path")) # create the application instance
app.config.from_object(__name__) # load config from this file, cupboard.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.instance_path, 'cupboard.db'),
    DEBUG=True, # Set to false in production environment
    SECRET_KEY=config.get("app_config", "secret"),
    USERNAME=config.get("app_config", "username"),
    PASSWORD=config.get("app_config", "password")
))
app.config.from_envvar('CUPBOARD_SETTINGS', silent=True)


def connect_db():
    """Establish the database connection."""
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def get_db():
    """Open database connection if none exists."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    """Initialize the database."""
    db = get_db()
    with app.open_resources('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database from command line."""
    init_db()
    print("Database has been initialized.")


def query_db(query, args=(), one = False):
    """
        Queries the databases and returns first value if one is true, else returns
        all values.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        print("Database closed.")


"""This section contains functions to create the library of recipes."""

"""This section contains the views functions."""
@app.route('/')
def show_homepage():
    query = 'select id, name, type, prep_time from library'
    results = query_db(query)
    return render_template('home.html', entry=results)

"""
    This section contains functions to create an
    inventory and connect with external databases.
"""
