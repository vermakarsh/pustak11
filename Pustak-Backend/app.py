from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta, datetime
import os
from database import db

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pustakalay.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Initialize extensions
    db.init_app(app)
    
    # Enhanced CORS configuration for mobile connections
    CORS(app, 
         origins=['*'], 
         allow_headers=['*'], 
         methods=['*'],
         supports_credentials=True,
         expose_headers=['*'])
    
    # Add response headers for better connectivity
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Authorization')
        response.headers.add('Cache-Control', 'no-cache, no-store, must-revalidate')
        response.headers.add('Pragma', 'no-cache')
        response.headers.add('Expires', '0')
        return response
    
    JWTManager(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.books import books_bp
    from routes.donations import donations_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(donations_bp, url_prefix='/api/donations')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Add a simple test endpoint
    @app.route('/api/test')
    def test_endpoint():
        return {'message': 'API is working!', 'status': 'success', 'timestamp': str(datetime.now())}, 200
    
    # Add debug endpoint
    @app.route('/api/debug')
    def debug_endpoint():
        return {
            'message': 'Debug endpoint working', 
            'status': 'success',
            'backend_port': 9001,
            'cors_enabled': True
        }, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
