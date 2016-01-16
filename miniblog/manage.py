# -*- coding: utf-8 -*-
# @Date    : 2016-01-17 1:26
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

import sqlite3

from flask.ext.script import Manager

from miniblog import app

manager = Manager(app)


@manager.command
def init_db():
    """Initialize database
    """
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


if __name__ == "__main__":
    manager.run()
