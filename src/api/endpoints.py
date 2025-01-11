from flask import Blueprint, jsonify, request
from http import HTTPStatus
from config.extensions import db
from models.models import Appointment
from utilities.utilities import has_conflict
from datetime import datetime

home = Blueprint("/", __name__)


@home.route("/")
def index():
    return {"data": "OK"}



@home.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.get_json()
    doctor_id = data["doctor_id"]
    patient_name = data["patient_name"]
    start_time = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
    duration = data["duration"]

    #if no conflict then move to next step and create the appointment 
    conflict_message = has_conflict(doctor_id, start_time, duration)
    if conflict_message:
        return jsonify({"error": conflict_message}), HTTPStatus.CONFLICT

    
    new_appointment = Appointment(
        doctor_id=doctor_id,
        patient_name=patient_name,
        start_time=start_time,
        duration=duration,
    )
    db.session.add(new_appointment)
    db.session.commit()

    return new_appointment.json(), HTTPStatus.CREATED



@home.route("/appointments/<int:doctor_id>", methods=["GET"])
def get_appointments(doctor_id):
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    if not start_time or not end_time:
        return (
            jsonify({"error": "Both start_time and end_time are required"}),
            HTTPStatus.BAD_REQUEST,
        )
    


    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    #Returns all appointments  within that time window
    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.start_time >= start_time,
        Appointment.start_time <= end_time,
    ).all()

    return {
        "appointments": [appointment.json() for appointment in appointments]
    }, HTTPStatus.OK


@home.route("/appointments/first_available/<int:doctor_id>", methods=["GET"])
def get_first_available_appointment(doctor_id):
    start_time = request.args.get("start_time")

    if not start_time:
        return jsonify({"error": "start_time is required"}), HTTPStatus.BAD_REQUEST

    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

    #filter for appointments with that specific doctor within that time window
    appointment = (
        Appointment.query.filter(
            Appointment.doctor_id == doctor_id, Appointment.start_time >= start_time
        )
        .order_by(Appointment.start_time)
        .first()
    )

    if appointment:
        return {"appointment": appointment.json()}, HTTPStatus.OK
    else:
        return {
            "message": "No available appointments found after the specified time"
        }, HTTPStatus.NOT_FOUND
