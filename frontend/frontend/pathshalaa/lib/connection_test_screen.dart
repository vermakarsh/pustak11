import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

class ConnectionTestScreen extends StatefulWidget {
  @override
  _ConnectionTestScreenState createState() => _ConnectionTestScreenState();
}

class _ConnectionTestScreenState extends State<ConnectionTestScreen> {
  String _results = '';
  bool _testing = false;

  Future<void> _testAllConnections() async {
    setState(() {
      _testing = true;
      _results = 'Testing connections...\n\n';
    });

    List<String> urlsToTest = [
      'http://localhost:9001/api/test',
      'http://127.0.0.1:9001/api/test',
      'http://10.0.2.2:9001/api/test',
      'http://192.168.1.100:9001/api/test', // Replace with your actual IP
    ];

    for (String url in urlsToTest) {
      await _testSingleUrl(url);
    }

    setState(() {
      _testing = false;
      _results += '\n=== TESTING COMPLETE ===\n';
      _results += 'Platform: ${Platform.operatingSystem}\n';
      _results += 'Use the working URL in your ApiConstants\n';
    });
  }

  Future<void> _testSingleUrl(String url) async {
    try {
      setState(() {
        _results += 'Testing: $url\n';
      });

      final response = await http.get(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
      ).timeout(Duration(seconds: 5));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _results += '✅ SUCCESS: ${data['message']}\n';
          _results += '   Status: ${response.statusCode}\n\n';
        });
      } else {
        setState(() {
          _results += '❌ FAILED: HTTP ${response.statusCode}\n';
          _results += '   Body: ${response.body}\n\n';
        });
      }
    } catch (e) {
      setState(() {
        _results += '❌ ERROR: $e\n\n';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Connection Test'),
        backgroundColor: Colors.blue,
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton(
              onPressed: _testing ? null : _testAllConnections,
              child: Text(_testing ? 'Testing...' : 'Test All Connections'),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.all(16),
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
              ),
            ),
            SizedBox(height: 20),
            Expanded(
              child: Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: SingleChildScrollView(
                  child: Text(
                    _results.isEmpty ? 'Click "Test All Connections" to start' : _results,
                    style: TextStyle(fontFamily: 'monospace', fontSize: 12),
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
