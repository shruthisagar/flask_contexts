from flask import Flask, request,session,g
from pymysql.cursors import DictCursor
from flaskext.mysql import MySQL

def create_app(test_config=None):
    app = Flask(__name__)
    mysql = MySQL(cursorclass=DictCursor)
    with app.app_context():
        mysql.init_app(app)
        @app.before_request
        def before_request():
            g.db = mysql.connect()
        
        @app.after_request
        def after_request(response):
            if g and g.db:
                g.db.commit()
            return response

        @app.errorhandler(Exception)
        def handle_generic_error(error):
            if g and g.db:
                g.db.rollback()
            import traceback
            traceback.print_exc()
            app.logger.error(error)
    return app