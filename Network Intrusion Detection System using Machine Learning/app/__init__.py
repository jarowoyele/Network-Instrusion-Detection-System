from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import jinja2


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

limiter = Limiter(key_func=get_remote_address)

def create_app():
    print(f"Current working directory: {os.getcwd()}")
    print(f"__file__ location: {os.path.abspath(__file__)}")
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    print(f"Computed template directory: {template_dir}")
    print(f"Template directory exists: {os.path.isdir(template_dir)}")
    print(f"dashboard.html exists: {os.path.isfile(os.path.join(template_dir, 'dashboard.html'))}")
    
    # app = Flask(__name__, template_folder=template_dir)

    # template_dir = os.path.join(template_dir, '../templates')
    
    app = Flask(__name__, 
            static_folder=os.path.abspath('static'),
            template_folder=os.path.abspath('templates'))
    app.config.from_object(Config)
    app.jinja_loader = jinja2.FileSystemLoader(template_dir)
    limiter.init_app(app)
    app.logger.error('An error occurred', exc_info=True)
    from app.routes import main
    app.register_blueprint(main)

    from app.logging import setup_logging
    setup_logging(app)

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app