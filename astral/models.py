import string
import os

from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def refresh(app):
    try:
        os.makedirs(app.config['ASTRAL_STORAGE'])
    except:
        pass
    db.init_app(app)
    db.drop_all()
    db.create_all()
    for root, project_dirs, _ in os.walk(app.config['ASTRAL_STORAGE']):
        for project_dir in project_dirs:
            db.session.add(Project.load(os.path.join(root, project_dir)))
        db.session.commit()
        return


class Project(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, index=True)
    directory = db.Column(db.Text, nullable=False)
    error = []

    @staticmethod
    def all():
        try:
            return Project.query.all()
        except:
            return []

    @staticmethod
    def load(path):
        p = Project()
        try:
            with open(os.path.join(path, 'details.json'), 'rb') as fd:
                details = json.loads(fd.read())
                p.name = details['name']
                for d in details['directory']:
                    if os.path.exists(d):
                        p.directory = d
                        break
                else:
                    p.directory = ''
                    p.error.append('Unable to find project location, please set the directory')
        except:
            p.name = os.path.basename(path)
            p.directory = ''
            p.error.append('Could not find project details')
        return p

    def save(self):
        path = os.path.join(
            current_app.config['ASTRAL_STORAGE'],
            filter(lambda c: c in string.letters, self.name))
        if os.path.isabs(path):
            try:
                with open(os.path.join(path, 'details.json'), 'rb') as fd:
                    details = json.loads(fd.read())
            except:
                details = {'directory': []}
            details['name'] = self.name
            if self.directory and self.directory not in details['directory']:
                details['directory'].append(self.directory)
            try:
                os.makedirs(path)
                with open(os.path.join(path, 'details.json'), 'wb') as fd:
                    fd.write(json.dumps(details))
            except:
                pass


class Task(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, index=True)
    script_path = db.Column(db.Text, nullable=False)
