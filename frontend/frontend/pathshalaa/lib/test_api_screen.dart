import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class TestApiScreen extends StatefulWidget {
  @override
  _TestApiScreenState createState() => _TestApiScreenState();
}

class _TestApiScreenState extends State<TestApiScreen> {
  String _status = 'Not tested';
  String _data = '';

  Future<void> _testApi() async {
    setState(() {
      _status = 'Testing...';
      _data = '';
    });

    try {
      // Test basic connectivity
      final testResponse = await http.get(
        Uri.parse('http://localhost:9001/api/test'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(Duration(seconds: 5));

      if (testResponse.statusCode == 200) {
        setState(() {
          _status = 'Basic API Connected ✅';
        });

        // Test donations endpoint
        final donationsResponse = await http.get(
          Uri.parse('http://localhost:9001/api/donations/test'),
          headers: {'Content-Type': 'application/json'},
        ).timeout(Duration(seconds: 10));

        if (donationsResponse.statusCode == 200) {
          final data = json.decode(donationsResponse.body);
          setState(() {
            _status = 'Donations API Working ✅';
            _data = 'Found ${data['data']?.length ?? 0} donations\n\n';
            
            if (data['data'] != null && data['data'].isNotEmpty) {
              for (var donation in data['data'].take(3)) {
                _data += 'Book: ${donation['bookTitle']}\n';
                _data += 'Author: ${donation['bookAuthor']}\n';
                _data += 'Status: ${donation['status']}\n';
                _data += 'Donor: ${donation['donor']['name']}\n\n';
              }
            }
          });
        } else {
          setState(() {
            _status = 'Donations API Failed ❌';
            _data = 'Status: ${donationsResponse.statusCode}\nBody: ${donationsResponse.body}';
          });
        }
      } else {
        setState(() {
          _status = 'Basic API Failed ❌';
          _data = 'Status: ${testResponse.statusCode}\nBody: ${testResponse.body}';
        });
      }
    } catch (e) {
      setState(() {
        _status = 'Connection Error ❌';
        _data = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('API Test'),
        backgroundColor: Colors.blue,
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton(
              onPressed: _testApi,
              child: Text('Test API Connection'),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.all(16),
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
              ),
            ),
            SizedBox(height: 20),
            Text(
              'Status: $_status',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            Expanded(
              child: Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: SingleChildScrollView(
                  child: Text(
                    _data.isEmpty ? 'No data' : _data,
                    style: TextStyle(fontFamily: 'monospace'),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
