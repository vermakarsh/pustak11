# Pustak-Op Project - 30 July 2025

Complete Book Donation Management System with Flutter Frontend and Python Flask Backend.

## 🚀 Project Structure

```
pustakop/
├── frontend/frontend/pathshalaa/     # Flutter Mobile App
│   ├── lib/
│   │   ├── screens/                  # Dashboard & Donation Screens
│   │   ├── services/                 # API Services & Connection Logic
│   │   └── models/                   # Data Models
│   └── pubspec.yaml                  # Flutter Dependencies
└── Pustak-Backend/                   # Python Flask API
    ├── app.py                        # Main Flask Application
    ├── routes/                       # API Endpoints
    │   ├── donations.py              # Donation CRUD Operations
    │   ├── auth.py                   # Authentication
    │   └── books.py                  # Book Management
    ├── database.py                   # SQLAlchemy Models
    └── requirements.txt              # Python Dependencies
```

## 📱 Frontend Features

- **Dashboard Screen**: Real-time donation statistics and book listing
- **Donate Book Screen**: Form to add new book donations
- **API Integration**: Automatic fallback mechanism for network connectivity
- **Hindi Language Support**: Complete UI in Hindi/Devanagari
- **Responsive Design**: Mobile-optimized interface

## 🖥️ Backend Features

- **Flask REST API**: Complete CRUD operations for books and donations
- **SQLite Database**: Local database with 5 pre-populated Hindi books
- **CORS Support**: Cross-origin requests enabled for mobile connectivity
- **Admin Panel**: User management and book approval system
- **Debug Logging**: Comprehensive logging for troubleshooting

## 📚 Pre-loaded Books

1. **गीता रहस्य** - बाल गंगाधर तिलक
2. **हरी घास के ये दिन** - फणीश्वरनाथ रेणु
3. **आपका बंटी** - मन्नू भंडारी
4. **चंद्रकांता** - देवकीनंदन खत्री
5. **रामायण** - महर्षि वाल्मीकि

## 🔧 Setup Instructions

### Backend Setup
```bash
cd Pustak-Backend
pip install -r requirements.txt
python run.py
```
Backend runs on: `http://localhost:9001`

### Frontend Setup
```bash
cd frontend/frontend/pathshalaa
flutter pub get
flutter run
```

## 🌐 Network Configuration

The app automatically detects and tries multiple connection URLs:
- `http://10.10.124.203:9001` (Computer's WiFi IP)
- `http://10.0.2.2:9001` (Android Emulator)
- `http://localhost:9001` (Desktop/Local)

## 📊 API Endpoints

- `GET /api/test` - Health check
- `GET /api/donations/test` - Get all donations (no auth required)
- `POST /api/donations` - Add new donation
- `GET /api/books` - List all books
- `POST /api/auth/login` - User authentication

## 🔐 Default Admin Credentials

- **Username**: admin
- **Password**: admin123
- **Email**: admin@pustakalay.com

## 🐛 Debugging

The app includes comprehensive debug logging:
- API connection attempts
- Network status
- Data loading states
- Error handling with fallback mechanisms

## 📱 Tested Platforms

- ✅ Android Physical Device
- ✅ Android Emulator
- ✅ Windows Desktop
- ✅ Cross-platform API connectivity

## 🎯 Key Achievements

- **Full-stack Implementation**: Complete Flutter + Flask integration
- **Network Resilience**: Multiple fallback URLs for connectivity
- **Data Persistence**: SQLite database with proper models
- **User Experience**: Hindi interface with smooth navigation
- **Debug Support**: Extensive logging for troubleshooting

---

**Developed on**: July 30, 2025  
**Status**: Production Ready ✅
