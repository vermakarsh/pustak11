from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    donated_books = db.relationship('DonatedBook', backref='donor', lazy=True)
    borrowed_books = db.relationship('BorrowedBook', backref='borrower', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    donated_copies = db.relationship('DonatedBook', backref='book', lazy=True)
    borrowed_copies = db.relationship('BorrowedBook', backref='book', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'category': self.category,
            'description': self.description,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'available_copies': len([db for db in self.donated_copies if db.is_available])
        }

class DonatedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    condition = db.Column(db.String(20), default='Good')  # New, Good, Fair, Poor
    is_available = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    donated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'donor_id': self.donor_id,
            'condition': self.condition,
            'is_available': self.is_available,
            'notes': self.notes,
            'donated_at': self.donated_at.isoformat() if self.donated_at else None,
            'book': self.book.to_dict() if self.book else None,
            'donor': self.donor.to_dict() if self.donor else None
        }

class BorrowedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    donated_book_id = db.Column(db.Integer, db.ForeignKey('donated_book.id'), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime)
    is_returned = db.Column(db.Boolean, default=False)
    
    # Relationship
    donated_book = db.relationship('DonatedBook', backref='borrowings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'borrower_id': self.borrower_id,
            'donated_book_id': self.donated_book_id,
            'borrowed_at': self.borrowed_at.isoformat() if self.borrowed_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'returned_at': self.returned_at.isoformat() if self.returned_at else None,
            'is_returned': self.is_returned,
            'book': self.book.to_dict() if self.book else None,
            'borrower': self.borrower.to_dict() if self.borrower else None
        }
