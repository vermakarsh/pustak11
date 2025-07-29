# Pustakalay API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Error Response Format
```json
{
  "error": "Error message description"
}
```

## Success Response Format
Most endpoints return data in the following format:
```json
{
  "message": "Success message",
  "data": { ... }
}
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

**Request Body:**
```json
{
  "username": "string (required)",
  "email": "string (required)",
  "password": "string (required, min 6 chars)",
  "phone": "string (optional)",
  "address": "string (optional)"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "access_token": "jwt_token_here",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "address": "123 Main St",
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Login
**POST** `/auth/login`

**Request Body:**
```json
{
  "username": "string (username or email)",
  "password": "string"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "access_token": "jwt_token_here",
  "user": { ... }
}
```

### Get Profile
**GET** `/auth/profile` 🔒

**Response (200):**
```json
{
  "user": { ... }
}
```

### Update Profile
**PUT** `/auth/profile` 🔒

**Request Body:**
```json
{
  "username": "string (optional)",
  "email": "string (optional)",
  "phone": "string (optional)",
  "address": "string (optional)",
  "password": "string (optional)"
}
```

### Change Password
**POST** `/auth/change-password` 🔒

**Request Body:**
```json
{
  "current_password": "string",
  "new_password": "string (min 6 chars)"
}
```

---

## Books Endpoints

### Get All Books
**GET** `/books`

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 10)
- `search` (string): Search in title, author, ISBN
- `category` (string): Filter by category
- `available_only` (boolean): Show only available books

**Response (200):**
```json
{
  "books": [
    {
      "id": 1,
      "title": "Book Title",
      "author": "Author Name",
      "isbn": "1234567890",
      "category": "Fiction",
      "description": "Book description",
      "image_url": "http://example.com/image.jpg",
      "is_available": true,
      "created_at": "2024-01-01T00:00:00",
      "available_copies": 3
    }
  ],
  "total": 50,
  "pages": 5,
  "current_page": 1,
  "per_page": 10,
  "has_next": true,
  "has_prev": false
}
```

### Get Book by ID
**GET** `/books/{book_id}`

### Create Book (Admin Only)
**POST** `/books` 🔒👑

**Request Body:**
```json
{
  "title": "string (required)",
  "author": "string (required)",
  "isbn": "string (optional)",
  "category": "string (optional)",
  "description": "string (optional)",
  "image_url": "string (optional)"
}
```

### Update Book (Admin Only)
**PUT** `/books/{book_id}` 🔒👑

### Delete Book (Admin Only)
**DELETE** `/books/{book_id}` 🔒👑

### Borrow Book
**POST** `/books/{book_id}/borrow` 🔒

### Get Borrowed Books
**GET** `/books/borrowed` 🔒

### Return Book
**POST** `/books/return/{borrowing_id}` 🔒

### Get Categories
**GET** `/books/categories`

---

## Donations Endpoints

### Donate Book
**POST** `/donations` 🔒

**Request Body:**
```json
{
  "title": "string (required)",
  "author": "string (required)",
  "isbn": "string (optional)",
  "category": "string (optional)",
  "description": "string (optional)",
  "image_url": "string (optional)",
  "condition": "string (New/Good/Fair/Poor, default: Good)",
  "notes": "string (optional)"
}
```

### Get My Donations
**GET** `/donations/my-donations` 🔒

### Get All Donations (Admin Only)
**GET** `/donations` 🔒👑

### Get Donation by ID
**GET** `/donations/{donation_id}` 🔒

### Update Donation
**PUT** `/donations/{donation_id}` 🔒

### Delete Donation
**DELETE** `/donations/{donation_id}` 🔒

### Get Donation Stats
**GET** `/donations/stats` 🔒

---

## Admin Endpoints

### Admin Dashboard
**GET** `/admin/dashboard` 🔒👑

**Response (200):**
```json
{
  "stats": {
    "total_users": 100,
    "total_books": 500,
    "total_donations": 300,
    "total_borrowings": 200,
    "active_borrowings": 50,
    "overdue_borrowings": 5
  }
}
```

### Get All Users
**GET** `/admin/users` 🔒👑

### Make User Admin
**POST** `/admin/users/{user_id}/make-admin` 🔒👑

### Remove Admin Rights
**POST** `/admin/users/{user_id}/remove-admin` 🔒👑

### Get All Borrowings
**GET** `/admin/borrowings` 🔒👑

**Query Parameters:**
- `status`: all, active, returned, overdue

### Force Return Book
**POST** `/admin/borrowings/{borrowing_id}/force-return` 🔒👑

---

## Status Codes

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden (Admin access required)
- `404` - Not Found
- `500` - Internal Server Error

---

## Legend
- 🔒 = Authentication required
- 👑 = Admin access required
