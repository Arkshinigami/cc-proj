#!/usr/bin/env python3
"""
Test script for NTA Expense Reimbursement System backend API endpoints
"""
import unittest
import requests
import json
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables from frontend .env file
load_dotenv('/app/frontend/.env')

# Get the backend URL from environment variables
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL')
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Testing API at: {API_BASE_URL}")

class TestNTAExpenseReimbursementAPI(unittest.TestCase):
    """Test cases for NTA Expense Reimbursement System API"""

    def test_01_api_health_check(self):
        """Test the API health check endpoint"""
        response = requests.get(f"{API_BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "NTA Expense Reimbursement System")
        print("✅ API health check passed")

    def test_02_cities_api(self):
        """Test the cities API endpoint"""
        response = requests.get(f"{API_BASE_URL}/cities")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cities", data)
        
        # Check if we have the expected cities from the seed data
        expected_cities = ['Ahmedabad', 'Kochi', 'Lucknow', 'Mumbai', 'New Delhi']
        self.assertEqual(sorted(data["cities"]), expected_cities)
        print(f"✅ Cities API passed, found cities: {data['cities']}")

    def test_03_record_retrieval_valid_city(self):
        """Test record retrieval with valid city"""
        # Test with Mumbai
        city = "Mumbai"
        response = requests.get(f"{API_BASE_URL}/reimbursement/city/{city}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify the record has all required fields
        self.assertEqual(data["city_assigned"], city)
        self.assertEqual(data["name"], "Priya Sharma")
        self.assertEqual(data["state"], "Maharashtra")
        self.assertIn("centre_no", data)
        self.assertIn("bank_name", data)
        self.assertIn("ifsc", data)
        self.assertIn("bank_account_number", data)
        print(f"✅ Record retrieval for city '{city}' passed")
        
        # Test with Ahmedabad
        city = "Ahmedabad"
        response = requests.get(f"{API_BASE_URL}/reimbursement/city/{city}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["city_assigned"], city)
        self.assertEqual(data["name"], "Suresh Patel")
        print(f"✅ Record retrieval for city '{city}' passed")

    def test_04_record_retrieval_invalid_city(self):
        """Test record retrieval with invalid city"""
        city = "InvalidCity"
        response = requests.get(f"{API_BASE_URL}/reimbursement/city/{city}")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("detail", data)
        print(f"✅ Record retrieval for invalid city '{city}' correctly returns 404")

    def test_05_record_update_valid(self):
        """Test record update with valid data"""
        # First get a record to update
        city = "Mumbai"
        response = requests.get(f"{API_BASE_URL}/reimbursement/city/{city}")
        self.assertEqual(response.status_code, 200)
        record = response.json()
        record_id = record["id"]
        
        # Prepare update data
        update_data = {
            "city_coordinator_claim": 5000.00,
            "observer_claim": 3000.00,
            "num_observers": 2,
            "refreshment_claim": 1500.00
        }
        
        # Update the record
        response = requests.put(
            f"{API_BASE_URL}/reimbursement/{record_id}",
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        updated_record = response.json()
        
        # Verify the updates
        self.assertEqual(updated_record["city_coordinator_claim"], 5000.00)
        self.assertEqual(updated_record["observer_claim"], 3000.00)
        self.assertEqual(updated_record["num_observers"], 2)
        self.assertEqual(updated_record["refreshment_claim"], 1500.00)
        
        # Verify updated_at timestamp is set
        self.assertIn("updated_at", updated_record)
        print(f"✅ Record update for ID '{record_id}' passed")

    def test_06_record_update_invalid(self):
        """Test record update with invalid record ID"""
        invalid_id = "invalid-uuid-that-does-not-exist"
        update_data = {
            "city_coordinator_claim": 5000.00
        }
        
        response = requests.put(
            f"{API_BASE_URL}/reimbursement/{invalid_id}",
            json=update_data
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("detail", data)
        print(f"✅ Record update for invalid ID correctly returns 404")

    def test_07_file_upload_and_download(self):
        """Test file upload and download functionality"""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(b"This is a test file for NTA Expense Reimbursement System")
            temp_file_path = temp_file.name
        
        try:
            # Upload the file
            with open(temp_file_path, "rb") as file:
                response = requests.post(
                    f"{API_BASE_URL}/upload",
                    files={"file": (os.path.basename(temp_file_path), file)}
                )
            
            self.assertEqual(response.status_code, 200)
            upload_data = response.json()
            self.assertIn("filename", upload_data)
            self.assertIn("original_name", upload_data)
            self.assertIn("size", upload_data)
            
            filename = upload_data["filename"]
            
            # Download the file
            response = requests.get(f"{API_BASE_URL}/download/{filename}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, b"This is a test file for NTA Expense Reimbursement System")
            
            print(f"✅ File upload and download passed")
            
            # Test download with invalid filename
            response = requests.get(f"{API_BASE_URL}/download/invalid-filename.txt")
            self.assertEqual(response.status_code, 404)
            print(f"✅ File download with invalid filename correctly returns 404")
            
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_08_database_seeding(self):
        """Verify that sample data was properly seeded"""
        # Get all cities and check count
        response = requests.get(f"{API_BASE_URL}/cities")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["cities"]), 5)
        
        # Check each city has a valid record
        cities = ['Ahmedabad', 'Kochi', 'Lucknow', 'Mumbai', 'New Delhi']
        for city in cities:
            response = requests.get(f"{API_BASE_URL}/reimbursement/city/{city}")
            self.assertEqual(response.status_code, 200)
            record = response.json()
            self.assertEqual(record["city_assigned"], city)
            
        print(f"✅ Database seeding verification passed")

if __name__ == "__main__":
    unittest.main(verbosity=2)