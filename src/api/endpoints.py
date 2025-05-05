from flask import Blueprint, jsonify, request
from http import HTTPStatus
from config.extensions import db
from models.models import Appointment
from utilities.utilities import has_conflict
from datetime import datetime

home = Blueprint("/", __name__)

@home.route("/")
def index():
    return jsonify({"status": "OK"}), HTTPStatus.OK


def parse_datetime(dt_str, field_name):
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        raise ValueError(f"Invalid format for '{field_name}'. Use 'YYYY-MM-DD HH:MM:SS'")


@home.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.get_json()

    required_fields = ["doctor_id", "patient_name", "start_time", "duration"]
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), HTTPStatus.BAD_REQUEST

    try:
        doctor_id = int(data["doctor_id"])
        patient_name = str(data["patient_name"]).strip()
        start_time = parse_datetime(data["start_time"], "start_time")
        duration = int(data["duration"])
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    conflict = has_conflict(doctor_id, start_time, duration)
    if conflict:
        return jsonify({"error": conflict}), HTTPStatus.CONFLICT

    new_appointment = Appointment(
        doctor_id=doctor_id,
        patient_name=patient_name,
        start_time=start_time,
        duration=duration
    )

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify(new_appointment.json()), HTTPStatus.CREATED


@home.route("/appointments/<int:doctor_id>", methods=["GET"])
def get_appointments(doctor_id):
    start_time_str = request.args.get("start_time")
    end_time_str = request.args.get("end_time")

    if not start_time_str or not end_time_str:
        return jsonify({"error": "Both 'start_time' and 'end_time' query parameters are required."}), HTTPStatus.BAD_REQUEST

    try:
        start_time = parse_datetime(start_time_str, "start_time")
        end_time = parse_datetime(end_time_str, "end_time")
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.start_time.between(start_time, end_time)
    ).order_by(Appointment.start_time.asc()).all()

    return jsonify({"appointments": [a.json() for a in appointments]}), HTTPStatus.OK


@home.route("/appointments/first_available/<int:doctor_id>", methods=["GET"])
def get_first_available_appointment(doctor_id):
    start_time_str = request.args.get("start_time")
    if not start_time_str:
        return jsonify({"error": "'start_time' query parameter is required."}), HTTPStatus.BAD_REQUEST

    try:
        start_time = parse_datetime(start_time_str, "start_time")
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    appointment = (
        Appointment.query
        .filter(Appointment.doctor_id == doctor_id, Appointment.start_time >= start_time)
        .order_by(Appointment.start_time.asc())
        .first()
    )

    if appointment:
        return jsonify({"appointment": appointment.json()}), HTTPStatus.OK

    return jsonify({"message": "No available appointments found after the specified time."}), HTTPStatus.NOT_FOUND
