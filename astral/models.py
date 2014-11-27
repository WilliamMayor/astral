from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, index=True)
    directory = db.Column(db.Text, nullable=False)


class Task(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, index=True)
    script_path = db.Column(db.Text, nullable=False)
