# Quick API URLs Reference

## Auth Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update profile
- `POST /api/auth/change-password` - Change password

## Books Endpoints
- `GET /api/books` - Get all books (with filters)
- `GET /api/books/{id}` - Get book details
- `POST /api/books` - Create book (admin)
- `PUT /api/books/{id}` - Update book (admin)
- `DELETE /api/books/{id}` - Delete book (admin)
- `POST /api/books/{id}/borrow` - Borrow book
- `GET /api/books/borrowed` - Get my borrowed books
- `POST /api/books/return/{borrowing_id}` - Return book
- `GET /api/books/categories` - Get all categories

## Donations Endpoints
- `POST /api/donations` - Donate a book
- `GET /api/donations/my-donations` - Get my donations
- `GET /api/donations` - Get all donations (admin)
- `GET /api/donations/{id}` - Get donation details
- `PUT /api/donations/{id}` - Update donation
- `DELETE /api/donations/{id}` - Delete donation
- `GET /api/donations/stats` - Get donation statistics

## Admin Endpoints
- `GET /api/admin/dashboard` - Admin dashboard stats
- `GET /api/admin/users` - Get all users
- `POST /api/admin/users/{id}/make-admin` - Make user admin
- `POST /api/admin/users/{id}/remove-admin` - Remove admin rights
- `GET /api/admin/borrowings` - Get all borrowings
- `POST /api/admin/borrowings/{id}/force-return` - Force return book

## Base URL
```
http://localhost:5000
```

## Authentication Header
```
Authorization: Bearer <jwt_token>
```
