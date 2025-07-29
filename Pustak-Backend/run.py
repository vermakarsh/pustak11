from app import create_app, db

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create a default admin user
        from database import User
        
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@pustakalay.com',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created!")
            print("Username: admin")
            print("Password: admin123")
            print("Email: admin@pustakalay.com")
        else:
            print("Admin user already exists!")
    
    print("Starting server on http://localhost:9001")
    app.run(debug=True, host='0.0.0.0', port=9001)
