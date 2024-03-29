from flask.ext.assets import Environment, Bundle

assets = Environment()

css = Bundle(
    'css/main.scss',
    filters='scss,cssmin',
    output='main.min.css',
    depends=['css/*.scss', 'css/*/*.scss'])
assets.register('css', css)

js = Bundle(
    'js/vendor/jquery.js',
    'js/vendor/knockout.js',
    'js/vendor/underscore.js',
    Bundle(
        'js/flashes.js',
        filters='rjsmin'),
    output='main.min.js')
assets.register('js', js)
