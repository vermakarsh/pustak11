from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db, User, Book, DonatedBook, BorrowedBook
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get statistics
        total_users = User.query.count()
        total_books = Book.query.count()
        total_donations = DonatedBook.query.count()
        total_borrowings = BorrowedBook.query.count()
        active_borrowings = BorrowedBook.query.filter_by(is_returned=False).count()
        overdue_borrowings = BorrowedBook.query.filter(
            BorrowedBook.is_returned == False,
            BorrowedBook.due_date < datetime.utcnow()
        ).count()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'total_books': total_books,
                'total_donations': total_donations,
                'total_borrowings': total_borrowings,
                'active_borrowings': active_borrowings,
                'overdue_borrowings': overdue_borrowings
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users = User.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': users.has_next,
            'has_prev': users.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/make-admin', methods=['POST'])
@jwt_required()
def make_admin(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        target_user = User.query.get(user_id)
        
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        target_user.is_admin = True
        db.session.commit()
        
        return jsonify({
            'message': f'User {target_user.username} is now an admin'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/remove-admin', methods=['POST'])
@jwt_required()
def remove_admin(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        if current_user_id == user_id:
            return jsonify({'error': 'Cannot remove admin rights from yourself'}), 400
        
        target_user = User.query.get(user_id)
        
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        target_user.is_admin = False
        db.session.commit()
        
        return jsonify({
            'message': f'Admin rights removed from {target_user.username}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/borrowings', methods=['GET'])
@jwt_required()
def get_all_borrowings():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', 'all')  # all, active, returned, overdue
        
        query = BorrowedBook.query
        
        if status == 'active':
            query = query.filter_by(is_returned=False)
        elif status == 'returned':
            query = query.filter_by(is_returned=True)
        elif status == 'overdue':
            query = query.filter(
                BorrowedBook.is_returned == False,
                BorrowedBook.due_date < datetime.utcnow()
            )
        
        borrowings = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'borrowings': [borrowing.to_dict() for borrowing in borrowings.items],
            'total': borrowings.total,
            'pages': borrowings.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': borrowings.has_next,
            'has_prev': borrowings.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/borrowings/<int:borrowing_id>/force-return', methods=['POST'])
@jwt_required()
def force_return_book(borrowing_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        borrowing = BorrowedBook.query.get(borrowing_id)
        
        if not borrowing:
            return jsonify({'error': 'Borrowing record not found'}), 404
        
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
            'message': 'Book return forced successfully',
            'borrowing': borrowing.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
