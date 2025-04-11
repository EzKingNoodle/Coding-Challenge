# Import necessary libraries
from flask import Flask                    # Main Flask framework
from flask_sqlalchemy import SQLAlchemy   # Database ORM
from flask_jwt_extended import JWTManager # JWT authentication
from flask_migrate import Migrate         # Database migrations
from dotenv import load_dotenv            # Load environment variables
import os                                 # Operating system functions

# Load environment variables from .env file
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()        # Database interface
jwt = JWTManager()       # JWT authentication manager
migrate = Migrate()      # Database migration manager

def create_app():
    # Create Flask application instance
    app = Flask(__name__)
    
    # Configure application settings
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Database connection URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False               # Disable modification tracking
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')         # Secret key for JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600                      # Token expires in 1 hour
    
    # Initialize extensions with the app
    db.init_app(app)      # Set up database
    jwt.init_app(app)     # Set up JWT
    migrate.init_app(app, db)  # Set up migrations
    
    # JWT configuration
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user)  # Convert user ID to string for JWT
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]  # Get user ID from JWT
        return identity
    
    # Register API routes
    from routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')  # Add user routes
    
    # Create database tables
    with app.app_context():
        db.create_all()  # Create all database tables
    
    return app

# Run the application if this file is run directly
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)  # Start server in debug mode