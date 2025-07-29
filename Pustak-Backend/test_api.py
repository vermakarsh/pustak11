import requests
import json

# Test the donations API
url = "http://localhost:9001/api/donations"

try:
    # Test GET request (this would require authentication in real scenario)
    response = requests.get(url)
    
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Headers: {response.headers}")
    print(f"API Response Body: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n=== PARSED RESPONSE ===")
        print(f"Success: {data.get('success', 'Not specified')}")
        print(f"Data length: {len(data.get('data', []))}")
        
        if 'data' in data:
            for i, donation in enumerate(data['data'][:2]):  # Show first 2 donations
                print(f"\nDonation {i+1}:")
                print(f"  ID: {donation.get('id')}")
                print(f"  Donation ID: {donation.get('donationId')}")
                print(f"  Book: {donation.get('bookTitle')} by {donation.get('bookAuthor')}")
                print(f"  Genre: {donation.get('bookGenre')}")
                print(f"  Status: {donation.get('status')}")
                print(f"  Donor: {donation.get('donor', {}).get('name')}")
    
except requests.exceptions.ConnectionError:
    print("Could not connect to server. Make sure it's running on port 9001")
except Exception as e:
    print(f"Error: {e}")
