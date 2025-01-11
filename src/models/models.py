from flask import jsonify
from config.extensions import db
from datetime import datetime
import json


class Doctor(db.Model):
    __tablename__ = 'doctor'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def json(self) -> str:
        return json.dumps({'id': self.id, 'name': self.name})



class DoctorSchedule(db.Model):
    __tablename__ = 'doctorschedule'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    day_of_week = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)


    def json(self) -> str:
        return json.dumps({
            'id': self.id,
            'doctor_name': self.doctor_id,
            'day_of_week': self.day_of_week,
            'start_time': str(self.start_time),
            'end_time': str(self.end_time)
        })



class Appointment(db.Model):
    __tablename__ = 'appointment'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def json(self) -> str:
        return json.dumps({
            'id': self.id,
            'doctor_name': self.doctor_id,
            'patient_name': self.patient_name,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': self.duration
        })



