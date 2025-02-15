from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configurations
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app
