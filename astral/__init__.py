from flask import Flask

from . import assets, routes, models

def create_app(config=None):
    app = Flask('astral')
    app.config.from_object('astral.config.defaults')
    try:
        app.config.from_pyfile('config/local.py')
    except:
        app.config['NEEDS_SETUP'] = True
    if config is not None:
        app.config.update(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
    
    assets.assets.init_app(app)
    models.db.init_app(app)
    
    app.register_blueprint(routes.routes)
    return app