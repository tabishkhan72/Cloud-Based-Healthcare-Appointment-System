from datetime import datetime, time
import json
import pytest
from app import create_app, db
from models.models import DoctorSchedule, Appointment,Doctor
import pytest



@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            appointment1 = Appointment(doctor_id=10, patient_name="Patient 1", start_time=datetime(2023, 1, 1, 9, 0, 0), duration="1:00:00")
            appointment2 = Appointment(doctor_id=10, patient_name="Patient 2", start_time=datetime(2023, 1, 1, 10, 0, 0), duration="1:00:00")
            doctor = Doctor(id=9999, name="Dr. Test")
            schedule = DoctorSchedule(doctor_id=9999, day_of_week="Tuesday", start_time=time(9, 0, 0), end_time=time(17, 0, 0))
            db.session.add(doctor)
            db.session.add(schedule)
            db.session.add(appointment1)
            db.session.add(appointment2)
            db.session.commit()

            yield client

            # Teardown
            db.session.remove()
            db.drop_all()






def test_get_appointments(client):

  params = {
    "start_time": "2023-01-01 09:00:00",
    "end_time": "2023-01-01 10:00:00" 
  }

  response = client.get("/appointments/10", query_string=params)  

  assert response.status_code == 200
  data = response.get_json()
  assert "appointments" in data



def test_create_appointment(client):
    response = client.post(
        "/appointments",
        json={
            "doctor_id": 9999,
            "patient_name": "John Doe",
            "start_time": "2030-01-01 10:00:00",
            "duration": "1:00:00",
        },
    )
    assert response.status_code == 201

  

def test_get_first_available_appointment(client):
    doctor_id = 10
    start_time = "2022-12-01 09:00:00"

    response = client.get(f"/appointments/first_available/{doctor_id}?start_time={start_time}")

    assert response.status_code == 200
    data = response.get_json()
    appointment_data = json.loads(data["appointment"])

    #check if appointments are coming back
    assert "appointment" in data


    #Check if the returned appointment's start_time is after the specified start_time
    assert datetime.strptime(appointment_data["start_time"], '%Y-%m-%d %H:%M:%S') >= datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    




