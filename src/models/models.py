from datetime import datetime, time
from config.extensions import db


class Doctor(db.Model):
    """
    Represents a doctor entity.
    """
    __tablename__ = 'doctor'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    schedules = db.relationship('DoctorSchedule', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"<Doctor {self.name}>"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }


class DoctorSchedule(db.Model):
    """
    Represents a doctor's weekly schedule.
    """
    __tablename__ = 'doctorschedule'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    day_of_week = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, doctor_id: int, day_of_week: str, start_time: time, end_time: time):
        self.doctor_id = doctor_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self) -> str:
        return f"<Schedule {self.day_of_week} for Doctor ID {self.doctor_id}>"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None
        }


class Appointment(db.Model):
    """
    Represents a scheduled appointment between a doctor and a patient.
    """
    __tablename__ = 'appointment'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes

    def __init__(self, doctor_id: int, patient_name: str, start_time: datetime, duration: int):
        self.doctor_id = doctor_id
        self.patient_name = patient_name
        self.start_time = start_time
        self.duration = duration

    def __repr__(self) -> str:
        return f"<Appointment with Dr. {self.doctor.name if self.doctor else 'Unknown'} at {self.start_time}>"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'patient_name': self.patient_name,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'duration': self.duration
        }
