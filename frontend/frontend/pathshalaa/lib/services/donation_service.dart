import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api_constants.dart';

class DonationService {
  static final DonationService _instance = DonationService._internal();
  factory DonationService() => _instance;
  DonationService._internal();

  // Local data as backup (initially empty, populated from API)
  List<Map<String, dynamic>> _localDonations = [];

  bool _apiConnected = false;
  List<Map<String, dynamic>> _apiDonations = [];

  // Test API connection with fallback URLs
  Future<bool> testApiConnection() async {
    // Force try the computer IP first for mobile devices
    List<String> priorityUrls = [
      'http://10.10.124.203:9001/api/test', // Your computer's Wi-Fi IP
      'http://192.168.1.203:9001/api/test', // Common router pattern
      'http://192.168.0.203:9001/api/test', // Another common pattern
      '${ApiConstants.baseUrl}/api/test',   // Base URL
      ...ApiConstants.fallbackUrls.map((url) => '$url/api/test'), // All fallbacks
    ];
    
    print('=== TESTING API CONNECTION ===');
    print('Trying ${priorityUrls.length} different URLs...');
    
    for (String testUrl in priorityUrls) {
      bool connected = await _testSingleUrl(testUrl);
      if (connected) {
        print('✅ Successfully connected to: $testUrl');
        return true;
      }
    }

    print('❌ All connection attempts failed');
    return false;
  }

  Future<bool> _testSingleUrl(String url) async {
    try {
      print('Testing API connection to: $url');
      final response = await http.get(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 5)); // Faster timeout

      print('API Test Response from ${url}: ${response.statusCode}');
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('API Test Success: ${data['message']}');
        _apiConnected = true;
        return true;
      } else {
        print('API Test Failed: Status ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('API Test Error for $url: $e');
      return false;
    }
  }

  // Fetch donations from API with aggressive retry
  Future<List<Map<String, dynamic>>> fetchDonationsFromAPI() async {
    try {
      print('=== STARTING API FETCH ===');
      
      // Force try the computer IP first for mobile devices
      List<String> priorityUrls = [
        'http://10.10.124.203:9001', // Your computer's Wi-Fi IP
        'http://192.168.1.203:9001', // Common router pattern with your device number
        'http://192.168.0.203:9001', // Another common pattern
        ...ApiConstants.fallbackUrls, // Then try other fallbacks
      ];
      
      // Try all URLs aggressively
      for (String baseUrl in priorityUrls) {
        try {
          print('Trying to fetch from: $baseUrl/api/donations/test');
          
          final response = await http.get(
            Uri.parse('$baseUrl/api/donations/test'),
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
          ).timeout(const Duration(seconds: 8)); // Reduced timeout for faster retry

          print('Response Status from $baseUrl: ${response.statusCode}');
          
          if (response.statusCode == 200) {
            final responseData = json.decode(response.body);
            print('SUCCESS! Got data from $baseUrl');
            print('Response: $responseData');
            
            if (responseData['status'] == 'success' && responseData['data'] != null) {
              List<dynamic> donations = responseData['data'];
              _apiDonations = donations.cast<Map<String, dynamic>>();
              _localDonations = _apiDonations;
              _apiConnected = true;
              
              print('✅ API FETCH SUCCESS: ${_apiDonations.length} donations loaded from $baseUrl');
              return _apiDonations;
            }
          }
        } catch (e) {
          print('❌ Failed to connect to $baseUrl: $e');
          continue; // Try next URL
        }
      }

      print('❌ ALL API ATTEMPTS FAILED - Using sample data');
      _apiConnected = false;
      _localDonations = _getSampleData();
      return _localDonations;
    } catch (e) {
      print('Network Error: $e');
      print('Using sample data as fallback');
      _localDonations = _getSampleData();
      return _localDonations;
    }
  }

  // Get sample data as fallback
  List<Map<String, dynamic>> _getSampleData() {
    print('🔴 === USING SAMPLE DATA ===');
    print('🔴 This means API connection failed!');
    print('🔴 Backend has real data but Flutter app cannot connect');
    print('🔴 Check network settings and IP configuration');
    
    _localDonations = [
      {
        'id': 1,
        'donationId': 'DON000001',
        'bookTitle': 'गीता रहस्य',
        'bookAuthor': 'बाल गंगाधर तिलक',
        'bookGenre': 'धर्म',
        'bookDescription': 'भगवद्गीता की व्याख्या',
        'bookCondition': 'Good',
        'bookIsbn': '978-8171234567',
        'bookLanguage': 'Hindi',
        'status': 'approved',
        'createdAt': '2025-07-29T18:03:00.895761',
        'donor': {'name': 'admin', 'email': 'admin@example.com'}
      },
      {
        'id': 2,
        'donationId': 'DON000002',
        'bookTitle': 'हरी घास के ये दिन',
        'bookAuthor': 'फणीश्वरनाथ रेणु',
        'bookGenre': 'उपन्यास',
        'bookDescription': 'प्रसिद्ध हिंदी उपन्यास',
        'bookCondition': 'Good',
        'bookIsbn': '978-8171234568',
        'bookLanguage': 'Hindi',
        'status': 'approved',
        'createdAt': '2025-07-29T18:03:00.900282',
        'donor': {'name': 'admin', 'email': 'admin@example.com'}
      },
      {
        'id': 3,
        'donationId': 'DON000003',
        'bookTitle': 'आपका बंटी',
        'bookAuthor': 'मन्नू भंडारी',
        'bookGenre': 'उपन्यास',
        'bookDescription': 'बाल मनोविज्ञान पर आधारित उपन्यास',
        'bookCondition': 'Good',
        'bookIsbn': '978-8171234569',
        'bookLanguage': 'Hindi',
        'status': 'approved',
        'createdAt': '2025-07-29T18:03:00.906341',
        'donor': {'name': 'admin', 'email': 'admin@example.com'}
      },
      {
        'id': 4,
        'donationId': 'DON000004',
        'bookTitle': 'चंद्रकांता',
        'bookAuthor': 'देवकीनंदन खत्री',
        'bookGenre': 'तिलिस्मी',
        'bookDescription': 'प्रसिद्ध तिलिस्मी उपन्यास',
        'bookCondition': 'Good',
        'bookIsbn': '978-8171234570',
        'bookLanguage': 'Hindi',
        'status': 'approved',
        'createdAt': '2025-07-29T18:03:00.909680',
        'donor': {'name': 'admin', 'email': 'admin@example.com'}
      },
      {
        'id': 5,
        'donationId': 'DON000005',
        'bookTitle': 'रामायण',
        'bookAuthor': 'महर्षि वाल्मीकि',
        'bookGenre': 'धर्म',
        'bookDescription': 'महाकाव्य रामायण',
        'bookCondition': 'Good',
        'bookIsbn': '978-8171234571',
        'bookLanguage': 'Hindi',
        'status': 'approved',
        'createdAt': '2025-07-29T18:03:00.911447',
        'donor': {'name': 'admin', 'email': 'admin@example.com'}
      }
    ];
    
    return _localDonations;
  }

  // Get donations (fetch from API and update local cache)
  List<Map<String, dynamic>> getDonations() {
    // Start background API fetch to get latest data
    fetchDonationsFromAPI().then((data) {
      // This will update _localDonations with fresh API data
    });
    
    // Return current local cache (which gets updated by API calls)
    return _localDonations;
  }

  // Get donations asynchronously - AGGRESSIVE CONNECTION METHOD
  Future<List<Map<String, dynamic>>> getDonationsAsync() async {
    print('🚀 === DONATION SERVICE: STARTING ===');
    
    // FORCE connection attempt with more IPs
    List<String> forceUrls = [
      'http://10.10.124.203:9001',  // Your computer's IP
      'http://192.168.1.203:9001',  // Router pattern 1
      'http://192.168.0.203:9001',  // Router pattern 2  
      'http://10.0.2.2:9001',       // Android emulator
      'http://172.16.0.203:9001',   // Corporate network pattern
    ];
    
    for (String baseUrl in forceUrls) {
      try {
        print('🔗 TRYING: $baseUrl/api/donations/test');
        
        final response = await http.get(
          Uri.parse('$baseUrl/api/donations/test'),
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
        ).timeout(const Duration(seconds: 5));
        
        print('📡 Response from $baseUrl: ${response.statusCode}');
        
        if (response.statusCode == 200) {
          final responseData = json.decode(response.body);
          print('✅ SUCCESS! Connected to $baseUrl');
          print('📋 Response structure: ${responseData.keys}');
          
          if (responseData['status'] == 'success' && responseData['data'] != null) {
            List<dynamic> donations = responseData['data'];
            _apiDonations = donations.cast<Map<String, dynamic>>();
            _localDonations = _apiDonations;
            _apiConnected = true;
            
            print('🎉 LOADED ${_apiDonations.length} REAL DONATIONS FROM API!');
            print('📖 First book: ${_apiDonations.isNotEmpty ? _apiDonations[0]['bookTitle'] : 'None'}');
            return _apiDonations;
          }
        }
      } catch (e) {
        print('❌ FAILED $baseUrl: $e');
        continue;
      }
    }
    
    // Fallback ke liye existing method call kar
    print('⚠️ ALL FORCE ATTEMPTS FAILED - Trying fallback method');
    return await fetchDonationsFromAPI();
  }

  // Add new donation
  Future<bool> addDonation({
    required String bookName,
    required String author,
    required String donorName,
    required String category,
    String condition = 'Good',
    String? description,
  }) async {
    // Send to API first
    try {
      if (!_apiConnected) {
        await testApiConnection();
      }

      if (_apiConnected) {
        final response = await http.post(
          Uri.parse(ApiConstants.fullDonationsUrl),
          headers: {'Content-Type': 'application/json'},
          body: json.encode({
            'bookName': bookName,
            'author': author,
            'donorName': donorName,
            'category': category,
            'condition': condition,
            'description': description,
          }),
        ).timeout(const Duration(seconds: 10));

        if (response.statusCode == 201) {
          print('Successfully synced donation to API');
          // Refresh local data from API
          await fetchDonationsFromAPI();
          return true;
        } else {
          print('Failed to sync donation to API: ${response.statusCode}');
          return false;
        }
      } else {
        print('API not connected, cannot add donation');
        return false;
      }
    } catch (e) {
      print('Error syncing donation to API: $e');
      return false;
    }
  }

  // Remove donation
  bool removeDonation(int index) {
    if (index >= 0 && index < _localDonations.length) {
      _localDonations.removeAt(index);
      return true;
    }
    return false;
  }

  // Statistics methods
  int getTotalDonations() => _localDonations.length;
  
  int getPendingDonations() => 
      _localDonations.where((d) => d['status'] == 'समीक्षा में').length;
  
  int getApprovedDonations() => 
      _localDonations.where((d) => d['status'] == 'स्वीकृत').length;
  
  int getUniqueDonors() => 
      _localDonations.map((d) => d['donor']).toSet().length;

  // Refresh data
  Future<void> refreshData() async {
    await fetchDonationsFromAPI();
  }
}
