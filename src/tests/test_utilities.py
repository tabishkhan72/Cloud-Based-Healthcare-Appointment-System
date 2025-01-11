from datetime import datetime
import pytest
from app import create_app, db
from models.models import DoctorSchedule
from utilities.utilities import has_conflict


@pytest.fixture
def test_app():
    app = create_app()
    with app.app_context():
        yield app

def test_has_conflict_not_working_day(test_app):
    """Test conflict when doctor is not working on the given day."""
    doctor_id = 1
    start_time = datetime.strptime("09:00", "%H:%M").time()
    end_time = datetime.strptime("17:00", "%H:%M").time()
    schedule = DoctorSchedule(doctor_id=doctor_id, day_of_week='Monday', start_time=start_time, end_time=end_time)
    db.session.add(schedule)
    db.session.commit()

    start_time = datetime.strptime('2023-10-17 10:00:00', '%Y-%m-%d %H:%M:%S') 
    duration = 30

    assert has_conflict(doctor_id, start_time, duration) == "Doctor not available on this day"

def test_has_conflict_outside_working_hours(test_app):
    """Test conflict when appointment time is outside of doctor's working hours."""
    doctor_id = 2
    start_time = datetime.strptime("09:00", "%H:%M").time()
    end_time = datetime.strptime("17:00", "%H:%M").time()
    schedule = DoctorSchedule(doctor_id=doctor_id, day_of_week='Wednesday', start_time=start_time, end_time=end_time)
    db.session.add(schedule)
    db.session.commit()

    start_time = datetime.strptime('2023-10-18 18:00:00', '%Y-%m-%d %H:%M:%S')
    duration = "1:00:00"

    assert has_conflict(doctor_id, start_time, duration) == "Appointment time falls outside doctor's working hours"


