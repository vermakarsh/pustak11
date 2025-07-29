from app import create_app
from database import db, DonatedBook, Book, User
from datetime import datetime

app = create_app()

with app.app_context():
    # Sample books data
    sample_books = [
        {
            'title': 'गीता रहस्य',
            'author': 'बाल गंगाधर तिलक',
            'category': 'धर्म',
            'description': 'भगवद्गीता की व्याख्या',
            'isbn': '978-8171234567'
        },
        {
            'title': 'हरी घास के ये दिन',
            'author': 'फणीश्वरनाथ रेणु',
            'category': 'उपन्यास',
            'description': 'प्रसिद्ध हिंदी उपन्यास',
            'isbn': '978-8171234568'
        },
        {
            'title': 'आपका बंटी',
            'author': 'मन्नू भंडारी',
            'category': 'उपन्यास',
            'description': 'बाल मनोविज्ञान पर आधारित उपन्यास',
            'isbn': '978-8171234569'
        },
        {
            'title': 'चंद्रकांता',
            'author': 'देवकीनंदन खत्री',
            'category': 'तिलिस्मी',
            'description': 'प्रसिद्ध तिलिस्मी उपन्यास',
            'isbn': '978-8171234570'
        },
        {
            'title': 'रामायण',
            'author': 'महर्षि वाल्मीकि',
            'category': 'धर्म',
            'description': 'महाकाव्य रामायण',
            'isbn': '978-8171234571'
        }
    ]
    
    # Get admin user
    admin_user = User.query.filter_by(username='admin').first()
    
    if not admin_user:
        print("Admin user not found!")
        exit()
    
    print("Adding sample books and donations...")
    
    for book_data in sample_books:
        # Check if book already exists
        existing_book = Book.query.filter_by(title=book_data['title']).first()
        
        if not existing_book:
            # Create new book
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                category=book_data['category'],
                description=book_data['description'],
                isbn=book_data['isbn']
            )
            db.session.add(book)
            db.session.flush()  # To get the book ID
            
            # Create donation for this book
            donation = DonatedBook(
                book_id=book.id,
                donor_id=admin_user.id,
                condition='Good',
                notes=f'Sample donation for {book_data["title"]}'
            )
            db.session.add(donation)
            
            print(f"Added: {book_data['title']} by {book_data['author']}")
        else:
            print(f"Book already exists: {book_data['title']}")
    
    db.session.commit()
    print(f"\nSample data added successfully!")
    
    # Show current data
    donations = DonatedBook.query.all()
    print(f"\nTotal donations in database: {len(donations)}")
    
    for d in donations:
        print(f"- {d.book.title} by {d.book.author} (Donated by: {d.donor.username})")
