"""
Script to seed the database with sample NTA reimbursement records
"""
import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Sample data for NTA reimbursement records
sample_records = [
    {
        "id": str(uuid.uuid4()),
        "sno": 1,
        "centre_no": "NTA001",
        "name": "Rajesh Kumar",
        "state": "Delhi",
        "city_assigned": "New Delhi",
        "mobile": "9876543210",
        "email": "rajesh.kumar@nta.gov.in",
        "num_exam_centres": 5,
        "bank_name": "State Bank of India",
        "ifsc": "SBIN0001234",
        "beneficiary_name": "Rajesh Kumar",
        "bank_account_number": "12345678901",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "sno": 2,
        "centre_no": "NTA002",
        "name": "Priya Sharma",
        "state": "Maharashtra",
        "city_assigned": "Mumbai",
        "mobile": "9876543211",
        "email": "priya.sharma@nta.gov.in",
        "num_exam_centres": 8,
        "bank_name": "HDFC Bank",
        "ifsc": "HDFC0001234",
        "beneficiary_name": "Priya Sharma",
        "bank_account_number": "12345678902",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "sno": 3,
        "centre_no": "NTA003",
        "name": "Suresh Patel",
        "state": "Gujarat",
        "city_assigned": "Ahmedabad",
        "mobile": "9876543212",
        "email": "suresh.patel@nta.gov.in",
        "num_exam_centres": 6,
        "bank_name": "Bank of Baroda",
        "ifsc": "BARB0001234",
        "beneficiary_name": "Suresh Patel",
        "bank_account_number": "12345678903",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "sno": 4,
        "centre_no": "NTA004",
        "name": "Lakshmi Nair",
        "state": "Kerala",
        "city_assigned": "Kochi",
        "mobile": "9876543213",
        "email": "lakshmi.nair@nta.gov.in",
        "num_exam_centres": 4,
        "bank_name": "Canara Bank",
        "ifsc": "CNRB0001234",
        "beneficiary_name": "Lakshmi Nair",
        "bank_account_number": "12345678904",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "sno": 5,
        "centre_no": "NTA005",
        "name": "Anil Singh",
        "state": "Uttar Pradesh",
        "city_assigned": "Lucknow",
        "mobile": "9876543214",
        "email": "anil.singh@nta.gov.in",
        "num_exam_centres": 7,
        "bank_name": "Punjab National Bank",
        "ifsc": "PUNB0001234",
        "beneficiary_name": "Anil Singh",
        "bank_account_number": "12345678905",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

async def seed_database():
    """Seed the database with sample records"""
    try:
        # Clear existing records
        await db.reimbursement_records.delete_many({})
        
        # Insert sample records
        result = await db.reimbursement_records.insert_many(sample_records)
        print(f"Inserted {len(result.inserted_ids)} sample records")
        
        # Verify the records
        count = await db.reimbursement_records.count_documents({})
        print(f"Total records in database: {count}")
        
        # List all cities
        cities = await db.reimbursement_records.distinct("city_assigned")
        print(f"Cities available: {cities}")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())