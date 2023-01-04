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
        UPLOAD_FOLDER=r'C:\Users\Boris\flask_myself_0\venv\Lib\site-packages\flaskr\static'
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    

    from flaskr import db
    db.init_app(app)

    from flaskr import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint='index')
    #app.add_url_rule("/", endpoint='blog.index')
    #app.add_url_rule("/", defaults={"page": 1}, endpoint="blog.index")#test
    #app.add_url_rule("/<int:page>", endpoint="blog.index")#test
    
    class RegexConverter(BaseConverter):
        def __init__(self, url_map, *items):
           super(RegexConverter, self).__init__(url_map)
           self.regex = items[0]
    app.url_map.converters['regex'] = RegexConverter

    #@app.route('/<regex("[abcABC0-9]{4,6}"):uid>-<slug>/')
    #def example(uid, slug):
        #return "uid: %s, slug: %s" % (uid, slug) #work exmaple stackoverflow guy

    #@app.route('/<regex("[abcABC0-9]{4,6}"):wrong_url>')
    #def example(wrong_url):
        #abort(401)
        #return f"<h1>{escape(wrong_url)}</h1>" #work my way
        
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/page_not_found.html'), 404
    return app