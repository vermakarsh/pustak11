from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db, Book, DonatedBook, BorrowedBook, User
from datetime import datetime, timedelta
from sqlalchemy import or_

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        available_only = request.args.get('available_only', 'false').lower() == 'true'
        
        query = Book.query
        
        # Search filter
        if search:
            query = query.filter(
                or_(
                    Book.title.ilike(f'%{search}%'),
                    Book.author.ilike(f'%{search}%'),
                    Book.isbn.ilike(f'%{search}%')
                )
            )
        
        # Category filter
        if category:
            query = query.filter(Book.category.ilike(f'%{category}%'))
        
        # Available only filter
        if available_only:
            query = query.filter(Book.is_available == True)
        
        # Pagination
        books = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'books': [book.to_dict() for book in books.items],
            'total': books.total,
            'pages': books.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': books.has_next,
            'has_prev': books.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Get available copies
        available_copies = DonatedBook.query.filter_by(
            book_id=book_id, 
            is_available=True
        ).all()
        
        book_data = book.to_dict()
        book_data['available_copies_detail'] = [copy.to_dict() for copy in available_copies]
        
        return jsonify({'book': book_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/', methods=['POST'])
@jwt_required()
def create_book():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        
        if not all([title, author]):
            return jsonify({'error': 'Title and author are required'}), 400
        
        # Check if book already exists (by title and author)
        existing_book = Book.query.filter_by(title=title, author=author).first()
        if existing_book:
            return jsonify({'error': 'Book already exists'}), 400
        
        book = Book(
            title=title,
            author=author,
            isbn=data.get('isbn', '').strip(),
            category=data.get('category', '').strip(),
            description=data.get('description', '').strip(),
            image_url=data.get('image_url', '').strip()
        )
        
        db.session.add(book)
        db.session.commit()
        
        return jsonify({
            'message': 'Book created successfully',
            'book': book.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        if 'title' in data:
            book.title = data['title'].strip()
        if 'author' in data:
            book.author = data['author'].strip()
        if 'isbn' in data:
            book.isbn = data['isbn'].strip()
        if 'category' in data:
            book.category = data['category'].strip()
        if 'description' in data:
            book.description = data['description'].strip()
        if 'image_url' in data:
            book.image_url = data['image_url'].strip()
        if 'is_available' in data:
            book.is_available = bool(data['is_available'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Book updated successfully',
            'book': book.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Check if book has any borrowed copies
        active_borrowings = BorrowedBook.query.filter_by(
            book_id=book_id, 
            is_returned=False
        ).count()
        
        if active_borrowings > 0:
            return jsonify({'error': 'Cannot delete book with active borrowings'}), 400
        
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({'message': 'Book deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>/borrow', methods=['POST'])
@jwt_required()
def borrow_book(book_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Check if user has any overdue books
        overdue_books = BorrowedBook.query.filter(
            BorrowedBook.borrower_id == user_id,
            BorrowedBook.is_returned == False,
            BorrowedBook.due_date < datetime.utcnow()
        ).count()
        
        if overdue_books > 0:
            return jsonify({'error': 'Please return overdue books before borrowing new ones'}), 400
        
        # Check if user already has this book
        existing_borrow = BorrowedBook.query.filter_by(
            book_id=book_id,
            borrower_id=user_id,
            is_returned=False
        ).first()
        
        if existing_borrow:
            return jsonify({'error': 'You have already borrowed this book'}), 400
        
        # Find an available donated copy
        available_copy = DonatedBook.query.filter_by(
            book_id=book_id,
            is_available=True
        ).first()
        
        if not available_copy:
            return jsonify({'error': 'No copies available for borrowing'}), 400
        
        # Create borrowing record
        due_date = datetime.utcnow() + timedelta(days=14)  # 2 weeks borrowing period
        
        borrowing = BorrowedBook(
            book_id=book_id,
            borrower_id=user_id,
            donated_book_id=available_copy.id,
            due_date=due_date
        )
        
        # Mark the donated copy as unavailable
        available_copy.is_available = False
        
        db.session.add(borrowing)
        db.session.commit()
        
        return jsonify({
            'message': 'Book borrowed successfully',
            'borrowing': borrowing.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/borrowed', methods=['GET'])
@jwt_required()
def get_borrowed_books():
    try:
        user_id = get_jwt_identity()
        
        borrowed_books = BorrowedBook.query.filter_by(
            borrower_id=user_id,
            is_returned=False
        ).all()
        
        return jsonify({
            'borrowed_books': [book.to_dict() for book in borrowed_books]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/return/<int:borrowing_id>', methods=['POST'])
@jwt_required()
def return_book(borrowing_id):
    try:
        user_id = get_jwt_identity()
        
        borrowing = BorrowedBook.query.get(borrowing_id)
        
        if not borrowing:
            return jsonify({'error': 'Borrowing record not found'}), 404
        
        if borrowing.borrower_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        if borrowing.is_returned:
            return jsonify({'error': 'Book already returned'}), 400
        
        # Mark as returned
        borrowing.is_returned = True
        borrowing.returned_at = datetime.utcnow()
        
        # Make the donated copy available again
        donated_copy = DonatedBook.query.get(borrowing.donated_book_id)
        if donated_copy:
            donated_copy.is_available = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'Book returned successfully',
            'borrowing': borrowing.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = db.session.query(Book.category).distinct().filter(
            Book.category.isnot(None),
            Book.category != ''
        ).all()
        
        category_list = [cat[0] for cat in categories if cat[0]]
        
        return jsonify({'categories': sorted(category_list)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
