# -*- coding: utf-8 -*-
# @Date    : 2016-01-16 23:18
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

import sqlite3

import os
from flask import Flask, g, render_template, session, abort, request, flash, redirect, url_for

app = Flask(__name__)

app.config.update(dict(
        DATABASE=os.path.join(os.path.dirname(__file__), 'miniblog.db'),
        DEBUG=True,
        SECRET_KEY='YouWillNeverGuessWithIt',
        USERNAME='admin',
        PASSWORD='password',
))


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT title, text FROM entries ORDER BY id DESC')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash(u'新增消息已经成功提交')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = u'无效用户'
        elif request.form['password'] != app.config['PASSWORD']:
            error = u'无效密码'
        else:
            session['logged_in'] = True
            flash(u'您已经成功登录')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(u'您已经成功注销')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    app.run()
