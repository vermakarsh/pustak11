from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db, DonatedBook, Book, User
from datetime import datetime

donations_bp = Blueprint('donations', __name__)

# Test endpoint without authentication - enhanced for mobile
@donations_bp.route('/test', methods=['GET', 'OPTIONS'])
def test_donations():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success', 'message': 'CORS preflight OK'}), 200
    
    try:
        print(f"[BACKEND] Test donations endpoint hit at {datetime.now()}")
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        donations = DonatedBook.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        print(f"[BACKEND] Found {donations.total} total donations in database")
        
        # Format the response to match frontend expectations
        donations_data = []
        for donation in donations.items:
            donation_dict = {
                'id': donation.id,
                'donationId': f"DON{donation.id:06d}",
                'bookTitle': donation.book.title if donation.book else '',
                'bookAuthor': donation.book.author if donation.book else '',
                'bookGenre': donation.book.category if donation.book else 'General',
                'bookDescription': donation.book.description if donation.book else '',
                'bookCondition': donation.condition,
                'bookIsbn': donation.book.isbn if donation.book else '',
                'bookLanguage': 'Hindi',  # Default language
                'status': 'approved',  # Default status
                'createdAt': donation.donated_at.isoformat() if donation.donated_at else None,
                'donor': {
                    'name': donation.donor.username if donation.donor else 'Unknown',
                    'email': donation.donor.email if donation.donor else ''
                }
            }
            donations_data.append(donation_dict)
        
        response_data = {
            'status': 'success',
            'message': f'Successfully fetched {len(donations_data)} donations',
            'data': donations_data,
            'meta': {
                'total': donations.total,
                'pages': donations.pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': donations.has_next,
                'has_prev': donations.has_prev
            }
        }
        
        print(f"[BACKEND] Returning {len(donations_data)} donations to frontend")
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"[BACKEND] Error in test_donations: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@donations_bp.route('/', methods=['POST'])
@jwt_required()
def donate_book():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        
        if not all([title, author]):
            return jsonify({'error': 'Title and author are required'}), 400
        
        # Check if book exists, if not create it
        book = Book.query.filter_by(title=title, author=author).first()
        
        if not book:
            book = Book(
                title=title,
                author=author,
                isbn=data.get('isbn', '').strip(),
                category=data.get('genre', data.get('category', 'General')).strip(),
                description=data.get('description', '').strip(),
                image_url=data.get('image_url', '').strip()
            )
            db.session.add(book)
            db.session.flush()  # To get the book ID
        
        # Create donation record
        donation = DonatedBook(
            book_id=book.id,
            donor_id=user_id,
            condition=data.get('condition', 'Good'),
            notes=data.get('notes', '').strip()
        )
        
        db.session.add(donation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Book donated successfully',
            'donation': donation.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@donations_bp.route('/my-donations', methods=['GET'])
@jwt_required()
def get_my_donations():
    try:
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        donations = DonatedBook.query.filter_by(donor_id=user_id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'donations': [donation.to_dict() for donation in donations.items],
            'total': donations.total,
            'pages': donations.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': donations.has_next,
            'has_prev': donations.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_donations():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Allow both admin and regular users to view donations
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        donations = DonatedBook.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Format the response to match frontend expectations
        donations_data = []
        for donation in donations.items:
            donation_dict = {
                'id': donation.id,
                'donationId': f"DON{donation.id:06d}",
                'bookTitle': donation.book.title if donation.book else '',
                'bookAuthor': donation.book.author if donation.book else '',
                'bookGenre': donation.book.category if donation.book else 'General',
                'bookDescription': donation.book.description if donation.book else '',
                'bookCondition': donation.condition,
                'bookIsbn': donation.book.isbn if donation.book else '',
                'bookLanguage': 'Hindi',  # Default language
                'status': 'approved',  # Default status
                'createdAt': donation.donated_at.isoformat() if donation.donated_at else None,
                'donor': {
                    'name': donation.donor.username if donation.donor else 'Unknown',
                    'email': donation.donor.email if donation.donor else ''
                }
            }
            donations_data.append(donation_dict)
        
        return jsonify({
            'success': True,
            'data': donations_data,
            'total': donations.total,
            'pages': donations.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': donations.has_next,
            'has_prev': donations.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@donations_bp.route('/<int:donation_id>', methods=['GET'])
@jwt_required()
def get_donation(donation_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        donation = DonatedBook.query.get(donation_id)
        
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        
        # Check if user can access this donation
        if not user.is_admin and donation.donor_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({'donation': donation.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/<int:donation_id>', methods=['PUT'])
@jwt_required()
def update_donation(donation_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        donation = DonatedBook.query.get(donation_id)
        
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        
        # Check if user can update this donation
        if not user.is_admin and donation.donor_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update allowed fields
        if 'condition' in data:
            donation.condition = data['condition']
        if 'notes' in data:
            donation.notes = data['notes'].strip()
        if 'is_available' in data and user.is_admin:
            donation.is_available = bool(data['is_available'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Donation updated successfully',
            'donation': donation.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/<int:donation_id>', methods=['DELETE'])
@jwt_required()
def delete_donation(donation_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        donation = DonatedBook.query.get(donation_id)
        
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        
        # Check if user can delete this donation
        if not user.is_admin and donation.donor_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Check if donation is currently borrowed
        if donation.borrowings and any(not b.is_returned for b in donation.borrowings):
            return jsonify({'error': 'Cannot delete donation that is currently borrowed'}), 400
        
        db.session.delete(donation)
        db.session.commit()
        
        return jsonify({'message': 'Donation deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_donation_stats():
    try:
        user_id = get_jwt_identity()
        
        # User's donation stats
        total_donated = DonatedBook.query.filter_by(donor_id=user_id).count()
        available_donated = DonatedBook.query.filter_by(
            donor_id=user_id, 
            is_available=True
        ).count()
        borrowed_donated = DonatedBook.query.filter_by(
            donor_id=user_id, 
            is_available=False
        ).count()
        
        return jsonify({
            'total_donated': total_donated,
            'available_donated': available_donated,
            'currently_borrowed': borrowed_donated
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
