


from datetime import timedelta
from models.models import Appointment, DoctorSchedule


def has_conflict(doctor_id, start_time, duration):
    """Check if there is a scheduling conflict for the given doctor at the given time."""
    day_of_week = start_time.strftime('%A')  # Get string
    schedule = DoctorSchedule.query.filter_by(doctor_id=doctor_id, day_of_week=day_of_week).first()

    

    if not schedule:
        return "Doctor not available on this day"
    

    hours, minutes, seconds = map(int, duration.split(':'))
    total_minutes = hours * 60 + minutes
    appointment_end_time = start_time + timedelta(minutes=total_minutes)
    
    #check if start time or end time falls outside the doctor's working hours
    if start_time.time() < schedule.start_time or appointment_end_time.time() > schedule.end_time:
        return "Appointment time falls outside doctor's working hours"
    

    #query for any overlapping appointments
    appointments = Appointment.query.filter(
    Appointment.doctor_id == doctor_id,
    Appointment.start_time < appointment_end_time,
    Appointment.start_time >= start_time
    ).all()

    #check if end times exceed proposed start time if so return a conflict error
    for appointment in appointments:
        appointment_end_time = appointment.start_time + timedelta(minutes=appointment.duration)
        if appointment_end_time > start_time:
            return "Appointment overlaps with another appointment"
    
    return None



