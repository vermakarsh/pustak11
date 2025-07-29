// API Configuration
class ApiConstants {
  // Base URL for the backend server
  // Try multiple URLs to ensure connection
  static String get baseUrl {
    // Always start with your computer's IP - this works for both emulator and physical device
    return 'http://10.10.124.203:9001';
  }

  // Alternative URLs to try if main one fails
  static List<String> get fallbackUrls => [
    'http://10.10.124.203:9001', // Your computer's IP - works best for mobile
    'http://192.168.1.203:9001', // Common router pattern with 203
    'http://192.168.0.203:9001', // Another router pattern with 203
    'http://192.168.1.100:9001', // Common router pattern
    'http://192.168.1.101:9001', // Another common pattern  
    'http://192.168.1.102:9001', // Another common pattern
    'http://192.168.0.100:9001', // Another common pattern
    'http://192.168.0.101:9001', // Another common pattern
    'http://10.0.2.2:9001',      // Android emulator - IMPORTANT
    'http://127.0.0.1:9001',     // Localhost
  ];
  
  // API endpoints
  static const String apiPrefix = '/api';
  
  // Donation endpoints
  static const String donations = '$apiPrefix/donations';
  static const String donationStats = '$donations/stats';
  
  // Auth endpoints
  static const String auth = '$apiPrefix/auth';
  static const String login = '$auth/login';
  static const String register = '$auth/register';
  
  // Book endpoints
  static const String books = '$apiPrefix/books';
  
  // User endpoints
  static const String users = '$apiPrefix/users';
  
  // Admin endpoints
  static const String admin = '$apiPrefix/admin';
  
  // Transaction endpoints
  static const String transactions = '$apiPrefix/transactions';
  
  // Certificate endpoints
  static const String certificates = '$apiPrefix/certificates';
  
  // Helper methods
  static String getDonationById(int id) => '$donations/$id';
  static String updateDonationStatus(int id) => '$donations/$id/status';
  static String deleteDonation(int id) => '$donations/$id';
  
  static String getBookById(int id) => '$books/$id';
  static String getUserById(int id) => '$users/$id';
  
  // Full URLs
  static String get fullDonationsUrl => '$baseUrl$donations';
  static String get fullDonationStatsUrl => '$baseUrl$donationStats';
  static String get fullLoginUrl => '$baseUrl$login';
  static String get fullRegisterUrl => '$baseUrl$register';
  static String get fullBooksUrl => '$baseUrl$books';
}
