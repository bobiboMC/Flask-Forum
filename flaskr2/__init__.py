import os

from flask import Flask
from werkzeug.routing import BaseConverter
from markupsafe import escape
from flask import abort
from flask import render_template



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER=r'YOUR UPLOAD PATH FOLDER'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from oauth2 import db
    db.init_app(app)

    from oauth2 import auth
    app.register_blueprint(auth.bp)

    from oauth2 import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint='index')
    
    class RegexConverter(BaseConverter):
        def __init__(self, url_map, *items):
           super(RegexConverter, self).__init__(url_map)
           self.regex = items[0]
    app.url_map.converters['regex'] = RegexConverter

        
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/page_not_found.html'), 404
    return app
