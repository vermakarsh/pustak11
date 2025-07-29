from app import create_app
from database import db, DonatedBook, Book, User

app = create_app()

with app.app_context():
    # Check donations
    donations = DonatedBook.query.all()
    print(f"Total donations in database: {len(donations)}")
    
    if donations:
        for d in donations:
            book_title = d.book.title if d.book else "Unknown"
            book_author = d.book.author if d.book else "Unknown"
            donor_name = d.donor.username if d.donor else "Unknown"
            print(f"Donation {d.id}: '{book_title}' by {book_author} - Donated by: {donor_name} - Date: {d.donated_at}")
    else:
        print("No donations found in database")
    
    # Check books
    books = Book.query.all()
    print(f"\nTotal books in database: {len(books)}")
    
    # Check users
    users = User.query.all()
    print(f"Total users in database: {len(users)}")
    for user in users:
        print(f"User: {user.username} - Email: {user.email} - Admin: {user.is_admin}")
