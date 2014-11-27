import os

from flask import Blueprint, render_template, current_app, flash, redirect, url_for

from .forms import SetupForm
from .models import Project

routes = Blueprint('routes', __name__, template_folder='templates')


@routes.before_request
def before_request():
    if current_app.config.get('NEEDS_SETUP', False):
        flash('Your Astral setup is incomplete, no project data will be saved', 'warn')

@routes.route('/')
def home():
    return render_template(
        'home.html')

@routes.route('/setup/', methods=['GET', 'POST'])
def setup():
    form = SetupForm(directory=current_app.config['ASTRAL_STORAGE'])
    if form.validate_on_submit():
        with open(os.path.join(current_app.root_path, 'config', 'local.py'), 'wb') as fd:
            for key, value in [('ASTRAL_STORAGE', form.directory.data)]:
                fd.write('%s=\'%s\'\n' % (key, value))
                current_app.config[key] = value
        current_app.config['NEEDS_SETUP'] = False
        return redirect(url_for('.home'))
    return render_template(
        'setup.html', form=form)