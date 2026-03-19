# main.py
from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
import math

# Initialize FastAPI app
app = FastAPI(
    title="Medical Appointment System",
    description="FastAPI backend for managing doctors, appointments, and consultations",
    version="1.0.0"
)

# ==================== DATA STORAGE ====================

# Doctors data - 6 initial doctors
doctors = [
    {"id": 1, "name": "Dr. Sarah Johnson", "specialization": "Cardiologist", "fee": 1500, "experience_years": 12, "is_available": True},
    {"id": 2, "name": "Dr. Michael Chen", "specialization": "Dermatologist", "fee": 1200, "experience_years": 8, "is_available": True},
    {"id": 3, "name": "Dr. Emily Rodriguez", "specialization": "Pediatrician", "fee": 1100, "experience_years": 10, "is_available": False},
    {"id": 4, "name": "Dr. David Kim", "specialization": "General", "fee": 800, "experience_years": 5, "is_available": True},
    {"id": 5, "name": "Dr. Lisa Patel", "specialization": "Cardiologist", "fee": 1800, "experience_years": 15, "is_available": True},
    {"id": 6, "name": "Dr. James Wilson", "specialization": "Dermatologist", "fee": 1300, "experience_years": 7, "is_available": False}
]

# Appointments storage
appointments = []
appt_counter = 1

# ==================== HELPER FUNCTIONS ====================

def find_doctor(doctor_id: int) -> Optional[Dict]:
    """Helper function to find a doctor by ID"""
    for doctor in doctors:
        if doctor["id"] == doctor_id:
            return doctor
    return None

def calculate_fee(base_fee: int, appointment_type: str, senior_citizen: bool = False) -> Dict[str, Any]:
    """
    Calculate consultation fee based on appointment type and senior citizen status
    - video: 80% of base fee
    - in-person: full fee
    - emergency: 150% of base fee
    - senior citizen: extra 15% discount after other calculations
    """
    # Base calculation based on appointment type
    if appointment_type == "video":
        calculated_fee = base_fee * 0.8
    elif appointment_type == "emergency":
        calculated_fee = base_fee * 1.5
    else:  # in-person
        calculated_fee = base_fee
    
    original_fee = calculated_fee
    
    # Apply senior citizen discount
    if senior_citizen:
        calculated_fee = calculated_fee * 0.85  # 15% discount
    
    return {
        "original_fee": round(original_fee, 2),
        "discount_applied": senior_citizen,
        "discount_amount": round(original_fee * 0.15, 2) if senior_citizen else 0,
        "final_fee": round(calculated_fee, 2)
    }

def filter_doctors_logic(
    doctors_list: List[Dict],
    specialization: Optional[str] = None,
    max_fee: Optional[int] = None,
    min_experience: Optional[int] = None,
    is_available: Optional[bool] = None
) -> List[Dict]:
    """Helper function to filter doctors based on multiple criteria"""
    filtered = doctors_list.copy()
    
    if specialization is not None:
        filtered = [d for d in filtered if d["specialization"].lower() == specialization.lower()]
    
    if max_fee is not None:
        filtered = [d for d in filtered if d["fee"] <= max_fee]
    
    if min_experience is not None:
        filtered = [d for d in filtered if d["experience_years"] >= min_experience]
    
    if is_available is not None:
        filtered = [d for d in filtered if d["is_available"] == is_available]
    
    return filtered

def find_appointment(appointment_id: int) -> Optional[Dict]:
    """Helper function to find an appointment by ID"""
    for appointment in appointments:
        if appointment["appointment_id"] == appointment_id:
            return appointment
    return None

def find_doctor_by_name(doctor_name: str) -> Optional[Dict]:
    """Helper to find doctor by name"""
    for doctor in doctors:
        if doctor["name"] == doctor_name:
            return doctor
    return None

# ==================== PYDANTIC MODELS ====================

class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2, description="Patient's full name")
    doctor_id: int = Field(..., gt=0, description="Doctor ID")
    date: str = Field(..., min_length=8, description="Appointment date (e.g., 2026-04-15)")
    reason: str = Field(..., min_length=5, description="Reason for appointment")
    appointment_type: str = Field(default="in-person", description="in-person, video, or emergency")
    senior_citizen: bool = Field(default=False, description="Whether patient is a senior citizen")
    
    @field_validator('appointment_type')
    def validate_appointment_type(cls, v):
        if v not in ["in-person", "video", "emergency"]:
            raise ValueError('appointment_type must be "in-person", "video", or "emergency"')
        return v
    
    @field_validator('date')
    def validate_date_format(cls, v):
        # Simple validation - in production use datetime
        if len(v) != 10 or v[4] != '-' or v[7] != '-':
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2, description="Doctor's full name")
    specialization: str = Field(..., min_length=2, description="Medical specialization")
    fee: int = Field(..., gt=0, description="Consultation fee in rupees")
    experience_years: int = Field(..., gt=0, description="Years of experience")
    is_available: bool = Field(default=True, description="Availability status")

class AppointmentStatusUpdate(BaseModel):
    status: str = Field(..., description="scheduled, confirmed, cancelled, completed")

# ==================== ROUTES ====================

# ========== HOME ROUTE (Always First) ==========
@app.get("/")
async def home():
    """Q1: Welcome message"""
    return {"message": "Welcome to MediCare Clinic"}

# ========== DOCTORS FIXED ROUTES (ALL FIXED ROUTES BEFORE VARIABLE) ==========
@app.get("/doctors")
async def get_all_doctors():
    """Q2: Get all doctors with total and available count"""
    total = len(doctors)
    available_count = sum(1 for d in doctors if d["is_available"])
    return {
        "doctors": doctors,
        "total": total,
        "available_count": available_count
    }

@app.get("/doctors/browse")
async def browse_doctors(
    # Search
    keyword: Optional[str] = Query(None, description="Search in name and specialization"),
    # Filters
    specialization: Optional[str] = Query(None, description="Filter by specialization"),
    max_fee: Optional[int] = Query(None, description="Maximum fee", gt=0),
    min_experience: Optional[int] = Query(None, description="Minimum experience", gt=0),
    is_available: Optional[bool] = Query(None, description="Filter by availability"),
    # Sort
    sort_by: str = Query("fee", description="fee, name, experience_years"),
    order: str = Query("asc", description="asc or desc"),
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(4, ge=1, le=10, description="Items per page")
):
    """Q20: Combined browse endpoint with search, filter, sort, pagination"""
    # Start with all doctors
    result_doctors = doctors.copy()
    
    # 1. Apply keyword search
    if keyword:
        keyword_lower = keyword.lower()
        result_doctors = [
            d for d in result_doctors
            if keyword_lower in d["name"].lower() or keyword_lower in d["specialization"].lower()
        ]
    
    # 2. Apply filters
    result_doctors = filter_doctors_logic(
        result_doctors,
        specialization=specialization,
        max_fee=max_fee,
        min_experience=min_experience,
        is_available=is_available
    )
    
    # 3. Apply sorting
    valid_sort_fields = ["fee", "name", "experience_years"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of {valid_sort_fields}")
    
    reverse = (order == "desc")
    
    if sort_by == "name":
        result_doctors = sorted(result_doctors, key=lambda d: d["name"], reverse=reverse)
    elif sort_by == "experience_years":
        result_doctors = sorted(result_doctors, key=lambda d: d["experience_years"], reverse=reverse)
    else:  # fee
        result_doctors = sorted(result_doctors, key=lambda d: d["fee"], reverse=reverse)
    
    # 4. Apply pagination
    total = len(result_doctors)
    total_pages = math.ceil(total / limit)
    
    start = (page - 1) * limit
    end = start + limit
    
    paginated_doctors = result_doctors[start:end]
    
    # Build response with all metadata
    response = {
        "filters_applied": {
            "keyword": keyword,
            "specialization": specialization,
            "max_fee": max_fee,
            "min_experience": min_experience,
            "is_available": is_available
        },
        "sorting": {
            "sort_by": sort_by,
            "order": order
        },
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        },
        "doctors": paginated_doctors
    }
    
    return response

@app.get("/doctors/filter")
async def filter_doctors(
    specialization: Optional[str] = Query(None, description="Filter by specialization"),
    max_fee: Optional[int] = Query(None, description="Maximum consultation fee", gt=0),
    min_experience: Optional[int] = Query(None, description="Minimum years of experience", gt=0),
    is_available: Optional[bool] = Query(None, description="Filter by availability")
):
    """Q10: Filter doctors based on multiple criteria"""
    filtered_doctors = filter_doctors_logic(
        doctors,
        specialization=specialization,
        max_fee=max_fee,
        min_experience=min_experience,
        is_available=is_available
    )
    
    return {
        "filters_applied": {
            "specialization": specialization,
            "max_fee": max_fee,
            "min_experience": min_experience,
            "is_available": is_available
        },
        "count": len(filtered_doctors),
        "doctors": filtered_doctors
    }

@app.get("/doctors/page")
async def paginate_doctors(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(3, ge=1, le=10, description="Items per page")
):
    """Q18: Paginate doctors list"""
    total = len(doctors)
    total_pages = math.ceil(total / limit)
    
    start = (page - 1) * limit
    end = start + limit
    
    paginated_doctors = doctors[start:end]
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "doctors": paginated_doctors
    }

@app.get("/doctors/search")
async def search_doctors(keyword: str = Query(..., min_length=1, description="Search keyword")):
    """Q16: Search doctors by name and specialization (case-insensitive)"""
    keyword_lower = keyword.lower()
    results = [
        d for d in doctors
        if keyword_lower in d["name"].lower() or keyword_lower in d["specialization"].lower()
    ]
    
    if not results:
        return {
            "message": f"No doctors found matching '{keyword}'",
            "total_found": 0,
            "doctors": []
        }
    
    return {
        "keyword": keyword,
        "total_found": len(results),
        "doctors": results
    }

@app.get("/doctors/sort")
async def sort_doctors(
    sort_by: str = Query("fee", description="Sort by: fee, name, experience_years"),
    order: str = Query("asc", description="Sort order: asc or desc")
):
    """Q17: Sort doctors by specified field"""
    # Validate sort_by
    valid_sort_fields = ["fee", "name", "experience_years"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by. Must be one of: {valid_sort_fields}"
        )
    
    # Validate order
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")
    
    # Sort doctors
    reverse = (order == "desc")
    
    if sort_by == "name":
        sorted_doctors = sorted(doctors, key=lambda d: d["name"], reverse=reverse)
    elif sort_by == "experience_years":
        sorted_doctors = sorted(doctors, key=lambda d: d["experience_years"], reverse=reverse)
    else:  # fee
        sorted_doctors = sorted(doctors, key=lambda d: d["fee"], reverse=reverse)
    
    return {
        "sort_by": sort_by,
        "order": order,
        "total": len(sorted_doctors),
        "doctors": sorted_doctors
    }

@app.get("/doctors/summary")
async def get_doctors_summary():
    """Q5: Summary statistics about doctors"""
    total_doctors = len(doctors)
    available_count = sum(1 for d in doctors if d["is_available"])
    
    # Find most experienced doctor
    most_experienced = max(doctors, key=lambda d: d["experience_years"]) if doctors else None
    
    # Find cheapest consultation fee
    cheapest_fee = min(doctors, key=lambda d: d["fee"])["fee"] if doctors else 0
    
    # Count per specialization
    specialization_count = {}
    for doctor in doctors:
        spec = doctor["specialization"]
        specialization_count[spec] = specialization_count.get(spec, 0) + 1
    
    return {
        "total_doctors": total_doctors,
        "available_count": available_count,
        "most_experienced_doctor": most_experienced["name"] if most_experienced else None,
        "most_experienced_years": most_experienced["experience_years"] if most_experienced else 0,
        "cheapest_consultation_fee": cheapest_fee,
        "specialization_breakdown": specialization_count
    }

# ========== DOCTORS VARIABLE ROUTE (LAST) ==========
@app.get("/doctors/{doctor_id}")
async def get_doctor_by_id(doctor_id: int):
    """Q3: Get doctor by ID"""
    doctor = find_doctor(doctor_id)
    if doctor is None:
        return {"error": "Doctor not found"}
    return doctor

# ========== APPOINTMENTS FIXED ROUTES ==========
@app.get("/appointments")
async def get_all_appointments():
    """Q4: Get all appointments with total count"""
    return {
        "appointments": appointments,
        "total": len(appointments)
    }

@app.get("/appointments/active")
async def get_active_appointments():
    """Q15: Get all active appointments (scheduled or confirmed)"""
    active = [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]
    return {
        "active_appointments": active,
        "total": len(active)
    }

@app.get("/appointments/by-doctor/{doctor_id}")
async def get_appointments_by_doctor(doctor_id: int):
    """Q15: Get all appointments for a specific doctor"""
    doctor = find_doctor(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    doctor_appointments = [a for a in appointments if a["doctor_name"] == doctor["name"]]
    return {
        "doctor_name": doctor["name"],
        "appointments": doctor_appointments,
        "total": len(doctor_appointments)
    }

@app.get("/appointments/page")
async def paginate_appointments(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(3, ge=1, le=10, description="Items per page")
):
    """Q19: Paginate appointments"""
    total = len(appointments)
    total_pages = math.ceil(total / limit)
    
    start = (page - 1) * limit
    end = start + limit
    
    paginated_appointments = appointments[start:end]
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "appointments": paginated_appointments
    }

@app.get("/appointments/search")
async def search_appointments(patient_name: str = Query(..., min_length=2, description="Patient name to search")):
    """Q19: Search appointments by patient name"""
    name_lower = patient_name.lower()
    results = [a for a in appointments if name_lower in a["patient_name"].lower()]
    
    return {
        "search_term": patient_name,
        "total_found": len(results),
        "appointments": results
    }

@app.get("/appointments/sort")
async def sort_appointments(
    sort_by: str = Query("fee", description="Sort by: fee, date"),
    order: str = Query("asc", description="asc or desc")
):
    """Q19: Sort appointments by fee or date"""
    if sort_by not in ["fee", "date"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'fee' or 'date'")
    
    reverse = (order == "desc")
    
    if sort_by == "fee":
        sorted_appointments = sorted(
            appointments, 
            key=lambda a: a["fee_details"]["final_fee"], 
            reverse=reverse
        )
    else:  # date - simple string comparison for demo
        sorted_appointments = sorted(
            appointments, 
            key=lambda a: a["date"], 
            reverse=reverse
        )
    
    return {
        "sort_by": sort_by,
        "order": order,
        "total": len(sorted_appointments),
        "appointments": sorted_appointments
    }

# ========== APPOINTMENTS VARIABLE ROUTE (if needed) ==========
# @app.get("/appointments/{appointment_id}")  # Add if you need this

# ========== POST ROUTES ==========
@app.post("/appointments", status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: AppointmentRequest):
    """Q6, Q7, Q8, Q9: Create a new appointment with validation"""
    global appt_counter
    
    # Check if doctor exists
    doctor = find_doctor(appointment.doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Check if doctor is available
    if not doctor["is_available"]:
        raise HTTPException(status_code=400, detail="Doctor is not available for new appointments")
    
    # Calculate fee using helper function
    fee_details = calculate_fee(
        doctor["fee"], 
        appointment.appointment_type,
        appointment.senior_citizen
    )
    
    # Create appointment
    new_appointment = {
        "appointment_id": appt_counter,
        "patient_name": appointment.patient_name,
        "doctor_name": doctor["name"],
        "doctor_specialization": doctor["specialization"],
        "date": appointment.date,
        "reason": appointment.reason,
        "appointment_type": appointment.appointment_type,
        "senior_citizen": appointment.senior_citizen,
        "base_fee": doctor["fee"],
        "fee_details": fee_details,
        "status": "scheduled"
    }
    
    appointments.append(new_appointment)
    appt_counter += 1
    
    return new_appointment

@app.post("/doctors", status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: NewDoctor):
    """Q11: Create a new doctor with duplicate name check"""
    # Check for duplicate name
    for existing in doctors:
        if existing["name"].lower() == doctor.name.lower():
            raise HTTPException(status_code=400, detail="Doctor with this name already exists")
    
    # Generate new ID
    new_id = max([d["id"] for d in doctors]) + 1 if doctors else 1
    
    new_doctor = doctor.model_dump()
    new_doctor["id"] = new_id
    
    doctors.append(new_doctor)
    return new_doctor


@app.post("/appointments/{appointment_id}/confirm")
async def confirm_appointment(appointment_id: int):  # ONLY appointment_id parameter
    """Q14: Confirm a scheduled appointment"""
    appointment = find_appointment(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if appointment["status"] != "scheduled":
        raise HTTPException(status_code=400, detail=f"Appointment is already {appointment['status']}")
    
    appointment["status"] = "confirmed"
    return appointment




@app.post("/appointments/{appointment_id}/cancel")
async def cancel_appointment(appointment_id: int):
    """Q14: Cancel an appointment and free up the doctor"""
    appointment = find_appointment(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if appointment["status"] in ["cancelled", "completed"]:
        raise HTTPException(status_code=400, detail=f"Appointment is already {appointment['status']}")
    
    # Update appointment status
    appointment["status"] = "cancelled"
    
    # Find and mark the doctor as available again
    doctor = find_doctor_by_name(appointment["doctor_name"])
    if doctor:
        doctor["is_available"] = True
    
    return appointment

@app.post("/appointments/{appointment_id}/complete")
async def complete_appointment(appointment_id: int):
    """Q15: Mark appointment as completed"""
    appointment = find_appointment(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if appointment["status"] != "confirmed":
        raise HTTPException(
            status_code=400, 
            detail=f"Only confirmed appointments can be completed (current status: {appointment['status']})"
        )
    
    appointment["status"] = "completed"
    
    # Find and mark the doctor as available for new appointments
    doctor = find_doctor_by_name(appointment["doctor_name"])
    if doctor:
        doctor["is_available"] = True
    
    return appointment

# ========== PUT/DELETE ROUTES ==========
@app.put("/doctors/{doctor_id}")
async def update_doctor(
    doctor_id: int,
    fee: Optional[int] = Query(None, description="Updated consultation fee", gt=0),
    is_available: Optional[bool] = Query(None, description="Updated availability status")
):
    """Q12: Update doctor's fee and/or availability"""
    doctor = find_doctor(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Update only non-None fields
    if fee is not None:
        doctor["fee"] = fee
    if is_available is not None:
        doctor["is_available"] = is_available
    
    return doctor

@app.delete("/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int):
    """Q13: Delete a doctor if no active appointments exist"""
    doctor = find_doctor(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Check if doctor has any scheduled appointments
    has_active_appointments = any(
        a["doctor_name"] == doctor["name"] and a["status"] in ["scheduled", "confirmed"]
        for a in appointments
    )
    
    if has_active_appointments:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete doctor with active appointments"
        )
    
    doctors.remove(doctor)
    return {"message": f"Doctor {doctor['name']} deleted successfully"}