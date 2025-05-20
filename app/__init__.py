from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize database
db = SQLAlchemy()

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'login'  # redirect to login page if not authenticated
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    
    # Secret key for sessions
    app.config['SECRET_KEY'] = 'bit2319'  # IMPORTANT: replace this with something secure in production
    
    # Database setup (SQLite file called site.db)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.models import User, Income, Expense
    
    with app.app_context():
        db.create_all()

    # Import routes here (late import to avoid circular import)
    from app.routes import routes
    app.register_blueprint(routes)

    return app 
