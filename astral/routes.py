import os

from flask import Blueprint, render_template, current_app, flash, redirect, url_for

import models
from .forms import SetupForm, ProjectForm
from .models import db, Project

routes = Blueprint('routes', __name__, template_folder='templates')


@routes.before_request
def before_request():
    if current_app.config.get('NEEDS_SETUP', False):
        flash('Your Astral setup is incomplete, no project data will be saved', 'warn')

@routes.route('/')
def home():
    return render_template(
        'home.html', projects=Project.all())

@routes.route('/setup/', methods=['GET', 'POST'])
def setup():
    form = SetupForm(directory=current_app.config['ASTRAL_STORAGE'])
    if form.validate_on_submit():
        with open(os.path.join(current_app.root_path, 'config', 'local.py'), 'wb') as fd:
            current_app.config['ASTRAL_STORAGE'] = form.directory.data
            current_app.config['DATABASE_URL'] = 'sqlite:///%s' % os.path.join(form.directory.data, 'astral.db')
            for k in ['ASTRAL_STORAGE', 'DATABASE_URL']:
                fd.write('%s="%s"\n' % (k, current_app.config[k]))
        # TODO: Make server reload (touch-reload)
        return redirect(url_for('.home'))
    return render_template(
        'setup.html', form=form)

@routes.route('/projects/', methods=['GET', 'POST'])
def projects_create():
    form = ProjectForm()
    if form.validate_on_submit():
        p = Project()
        form.populate_obj(p)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('.home'))
    return render_template(
        'projects/create.html', form=form)