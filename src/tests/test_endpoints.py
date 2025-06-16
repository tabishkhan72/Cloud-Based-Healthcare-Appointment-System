from datetime import datetime, time
import json
import pytest
from app import create_app, db
from models.models import DoctorSchedule, Appointment, Doctor

# --------------------
# Pytest Fixture Setup
# --------------------
@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Seed test data
            doctor = Doctor(id=9999, name="Dr. Test")
            schedule = DoctorSchedule(
                doctor_id=9999, 
                day_of_week="Tuesday", 
                start_time=time(9, 0, 0), 
                end_time=time(17, 0, 0)
            )
            appointment1 = Appointment(
                doctor_id=10,
                patient_name="Patient 1",
                start_time=datetime(2023, 1, 1, 9, 0, 0),
                duration="1:00:00"
            )
            appointment2 = Appointment(
                doctor_id=10,
                patient_name="Patient 2",
                start_time=datetime(2023, 1, 1, 10, 0, 0),
                duration="1:00:00"
            )

            db.session.add_all([doctor, schedule, appointment1, appointment2])
            db.session.commit()

            yield client

            db.session.remove()
            db.drop_all()

# --------------------
# Test: Get Appointments
# --------------------
def test_get_appointments(client):
    params = {
        "start_time": "2023-01-01 09:00:00",
        "end_time": "2023-01-01 10:00:00"
    }

    response = client.get("/appointments/10", query_string=params)
    assert response.status_code == 200, "Expected 200 OK"
    
    data = response.get_json()
    assert "appointments" in data, "'appointments' key not found in response"

# --------------------
# Test: Create Appointment
# --------------------
def test_create_appointment(client):
    payload = {
        "doctor_id": 9999,
        "patient_name": "John Doe",
        "start_time": "2030-01-01 10:00:00",
        "duration": "1:00:00"
    }

    response = client.post("/appointments", json=payload)
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"

# -------------------------------
# Test: Get First Available Slot
# -------------------------------
def test_get_first_available_appointment(client):
    doctor_id = 10
    start_time_str = "2022-12-01 09:00:00"
    start_time_dt = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')

    response = client.get(f"/appointments/first_available/{doctor_id}?start_time={start_time_str}")
    assert response.status_code == 200, "Expected 200 OK"

    data = response.get_json()
    assert "appointment" in data, "'appointment' key not found in response"

    appointment_data = json.loads(data["appointment"])
    returned_start_time = datetime.strptime(appointment_data["start_time"], '%Y-%m-%d %H:%M:%S')

    assert returned_start_time >= start_time_dt, "Returned appointment is earlier than requested start time"
