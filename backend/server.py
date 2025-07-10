from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import base64
import aiofiles


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create uploads directory
UPLOADS_DIR = ROOT_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class ReimbursementRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sno: Optional[int] = None
    
    # Basic Information - Excel Data (uneditable)
    city_code_excel: Optional[str] = None
    name_excel: Optional[str] = None
    state_excel: Optional[str] = None
    city_assigned_excel: Optional[str] = None
    mobile_excel: Optional[str] = None
    email_excel: Optional[str] = None
    num_exam_centres_excel: Optional[int] = None
    
    # Basic Information - User Input (editable)
    city_code_user: Optional[str] = None
    name_user: Optional[str] = None
    state_user: Optional[str] = None
    city_assigned_user: Optional[str] = None
    mobile_user: Optional[str] = None
    email_user: Optional[str] = None
    num_exam_centres_user: Optional[int] = None
    
    # Bank Details - Excel Data (uneditable)
    bank_name_excel: Optional[str] = None
    ifsc_excel: Optional[str] = None
    beneficiary_name_excel: Optional[str] = None
    bank_account_number_excel: Optional[str] = None
    
    # Bank Details - User Input (editable)
    bank_name_user: Optional[str] = None
    ifsc_user: Optional[str] = None
    beneficiary_name_user: Optional[str] = None
    bank_account_number_user: Optional[str] = None
    
    # Claim Fields - Excel Data (uneditable)
    city_coordinator_claim_excel: Optional[float] = None
    admin_staff_claim_excel: Optional[float] = None
    support_staff_claim_excel: Optional[float] = None
    refreshment_claim_excel: Optional[float] = None
    observer_claim_excel: Optional[float] = None
    num_observers_excel: Optional[int] = None
    claim_district_personnel_excel: Optional[float] = None
    assistant_staff_district_excel: Optional[float] = None
    support_staff_district_excel: Optional[float] = None
    claim_police_personnel_excel: Optional[float] = None
    support_staff_police_excel: Optional[float] = None
    duty_magistrate_claim_excel: Optional[float] = None
    num_duty_magistrates_excel: Optional[int] = None
    team_leader_claim_excel: Optional[float] = None
    num_team_leaders_excel: Optional[int] = None
    police_escort_claim_excel: Optional[float] = None
    num_police_escort_excel: Optional[int] = None
    police_frisking_claim_excel: Optional[float] = None
    num_police_frisking_excel: Optional[int] = None
    security_personnel_claim_excel: Optional[float] = None
    num_security_personnel_excel: Optional[int] = None
    bank_custodian_claim_excel: Optional[float] = None
    district_education_officer_claim_excel: Optional[float] = None
    support_staff_deo_claim_excel: Optional[float] = None
    
    # Claim Fields - User Input (editable)
    city_coordinator_claim_user: Optional[float] = None
    admin_staff_claim_user: Optional[float] = None
    support_staff_claim_user: Optional[float] = None
    refreshment_claim_user: Optional[float] = None
    observer_claim_user: Optional[float] = None
    num_observers_user: Optional[int] = None
    claim_district_personnel_user: Optional[float] = None
    assistant_staff_district_user: Optional[float] = None
    support_staff_district_user: Optional[float] = None
    claim_police_personnel_user: Optional[float] = None
    support_staff_police_user: Optional[float] = None
    duty_magistrate_claim_user: Optional[float] = None
    num_duty_magistrates_user: Optional[int] = None
    team_leader_claim_user: Optional[float] = None
    num_team_leaders_user: Optional[int] = None
    police_escort_claim_user: Optional[float] = None
    num_police_escort_user: Optional[int] = None
    police_frisking_claim_user: Optional[float] = None
    num_police_frisking_user: Optional[int] = None
    security_personnel_claim_user: Optional[float] = None
    num_security_personnel_user: Optional[int] = None
    bank_custodian_claim_user: Optional[float] = None
    district_education_officer_claim_user: Optional[float] = None
    support_staff_deo_claim_user: Optional[float] = None
    
    supporting_document_bills: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ReimbursementCreate(BaseModel):
    # Basic Information - User Input
    city_code_user: Optional[str] = None
    name_user: Optional[str] = None
    state_user: Optional[str] = None
    city_assigned_user: Optional[str] = None
    mobile_user: Optional[str] = None
    email_user: Optional[str] = None
    num_exam_centres_user: Optional[int] = None
    
    # Bank Details - User Input
    bank_name_user: Optional[str] = None
    ifsc_user: Optional[str] = None
    beneficiary_name_user: Optional[str] = None
    bank_account_number_user: Optional[str] = None
    
    # Claim Fields - User Input
    city_coordinator_claim_user: Optional[float] = None
    admin_staff_claim_user: Optional[float] = None
    support_staff_claim_user: Optional[float] = None
    refreshment_claim_user: Optional[float] = None
    observer_claim_user: Optional[float] = None
    num_observers_user: Optional[int] = None
    claim_district_personnel_user: Optional[float] = None
    assistant_staff_district_user: Optional[float] = None
    support_staff_district_user: Optional[float] = None
    claim_police_personnel_user: Optional[float] = None
    support_staff_police_user: Optional[float] = None
    duty_magistrate_claim_user: Optional[float] = None
    num_duty_magistrates_user: Optional[int] = None
    team_leader_claim_user: Optional[float] = None
    num_team_leaders_user: Optional[int] = None
    police_escort_claim_user: Optional[float] = None
    num_police_escort_user: Optional[int] = None
    police_frisking_claim_user: Optional[float] = None
    num_police_frisking_user: Optional[int] = None
    security_personnel_claim_user: Optional[float] = None
    num_security_personnel_user: Optional[int] = None
    bank_custodian_claim_user: Optional[float] = None
    district_education_officer_claim_user: Optional[float] = None
    support_staff_deo_claim_user: Optional[float] = None
    
    supporting_document_bills: Optional[str] = None

class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "NTA Expense Reimbursement System"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Get Excel template data (this would be fetched from OneDrive in real implementation)
@api_router.get("/template-data")
async def get_template_data():
    """Get template data from Excel (simulated - in real implementation this would fetch from OneDrive)"""
    try:
        # This would normally fetch from OneDrive Excel file
        # For now, returning sample template data
        template_data = {
            "city_code_excel": "MUM001",
            "name_excel": "John Doe",
            "state_excel": "Maharashtra",
            "city_assigned_excel": "Mumbai",
            "mobile_excel": "9876543210",
            "email_excel": "john.doe@nta.gov.in",
            "num_exam_centres_excel": 5,
            "bank_name_excel": "State Bank of India",
            "ifsc_excel": "SBIN0001234",
            "beneficiary_name_excel": "John Doe",
            "bank_account_number_excel": "12345678901",
            "city_coordinator_claim_excel": 5000.0,
            "admin_staff_claim_excel": 3000.0,
            "support_staff_claim_excel": 2000.0,
            "refreshment_claim_excel": 1500.0,
            "observer_claim_excel": 4000.0,
            "num_observers_excel": 3,
            "claim_district_personnel_excel": 2500.0,
            "assistant_staff_district_excel": 2000.0,
            "support_staff_district_excel": 1800.0,
            "claim_police_personnel_excel": 3000.0,
            "support_staff_police_excel": 2200.0,
            "duty_magistrate_claim_excel": 4500.0,
            "num_duty_magistrates_excel": 2,
            "team_leader_claim_excel": 3500.0,
            "num_team_leaders_excel": 4,
            "police_escort_claim_excel": 2800.0,
            "num_police_escort_excel": 6,
            "police_frisking_claim_excel": 2600.0,
            "num_police_frisking_excel": 8,
            "security_personnel_claim_excel": 3200.0,
            "num_security_personnel_excel": 10,
            "bank_custodian_claim_excel": 2400.0,
            "district_education_officer_claim_excel": 5500.0,
            "support_staff_deo_claim_excel": 2800.0
        }
        return template_data
    except Exception as e:
        logging.error(f"Error getting template data: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving template data")

# Create new reimbursement record
@api_router.post("/reimbursement", response_model=ReimbursementRecord)
async def create_reimbursement(input: ReimbursementCreate):
    """Create new reimbursement record"""
    try:
        record_dict = input.dict()
        record_obj = ReimbursementRecord(**record_dict)
        _ = await db.reimbursement_records.insert_one(record_obj.dict())
        return record_obj
    except Exception as e:
        logging.error(f"Error creating reimbursement: {e}")
        raise HTTPException(status_code=500, detail="Error creating reimbursement record")

@api_router.put("/reimbursement/{record_id}")
async def update_reimbursement(record_id: str, update_data: ReimbursementCreate):
    """Update reimbursement record"""
    try:
        update_dict = update_data.dict(exclude_unset=True)
        if update_dict:
            update_dict["updated_at"] = datetime.utcnow()
            
            result = await db.reimbursement_records.update_one(
                {"id": record_id},
                {"$set": update_dict}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Record not found")
            
            # Get updated record
            updated_record = await db.reimbursement_records.find_one({"id": record_id})
            updated_record.pop("_id", None)
            return updated_record
        else:
            raise HTTPException(status_code=400, detail="No data provided for update")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating reimbursement: {e}")
        raise HTTPException(status_code=500, detail="Error updating reimbursement record")

@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload for supporting documents"""
    try:
        # Generate unique filename
        file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
        unique_filename = f"{str(uuid.uuid4())}.{file_extension}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        content = await file.read()
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
        
        return {
            "filename": unique_filename,
            "original_name": file.filename,
            "size": len(content)
        }
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Error uploading file")

@api_router.get("/download/{filename}")
async def download_file(filename: str):
    """Download uploaded file"""
    try:
        file_path = UPLOADS_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail="Error downloading file")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
