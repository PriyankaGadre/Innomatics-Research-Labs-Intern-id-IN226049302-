# Medical Appointment System - FastAPI Backend

A complete FastAPI backend system for managing doctors, appointments, and consultations. Built as part of the FastAPI Internship Training.

## 🏥 Project Overview

This Medical Appointment System allows:
- Managing doctor profiles and availability
- Booking appointments with fee calculations
- Multi-step appointment workflow (schedule → confirm → complete)
- Advanced search, filtering, sorting, and pagination

## 🚀 Features Implemented

### Day 1: GET APIs
- Home route with welcome message
- List all doctors with counts
- Get doctor by ID
- List all appointments
- Summary statistics endpoint

### Day 2-3: POST + Pydantic + Helpers
- Appointment creation with validation
- Fee calculation based on appointment type (video/in-person/emergency)
- Senior citizen discounts
- Multi-criteria filtering

### Day 4: CRUD Operations
- Create new doctor with duplicate check
- Update doctor details
- Delete doctor (with active appointment check)
- Proper 201/404 status codes

### Day 5: Multi-step Workflow
- Confirm appointments
- Cancel appointments (frees up doctor)
- Complete appointments
- Get active appointments
- View appointments by doctor

### Day 6: Advanced Features
- Case-insensitive search (name + specialization)
- Sorting by fee, name, experience
- Pagination with total_pages
- Combined browse endpoint with search + filter + sort + pagination

## 🛠️ Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate