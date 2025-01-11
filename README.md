
### Appointment Scheduling System

This project implements a system for scheduling appointments with two doctors. Appointments can vary in length and are subject to the working hours of each doctor.

#### Models Implemented:

1. **Appointment Model:**
   - Represents an appointment with one of the two doctors.
   - Appointments can be of arbitrary length (e.g., 20 mins, 45 mins, 60 mins).

2. **Doctor Schedule Model:**
   - Represents the working hours of each doctor.
   - Doctor Strange works from 9 AM to 5 PM, Monday to Friday.
   - Doctor Who works from 8 AM to 4 PM, Monday to Friday.
   - Assumption: Working hours remain consistent every week.

#### Implemented APIs:

1. **Create Appointment API:**
   - Allows creating appointments, ensuring no conflicts with existing appointments.
   - Rejects appointment creation if there's a scheduling conflict.

2. **Get Appointments within Time Window API:**
   - Retrieves all appointments within a specified time window for a given doctor.
   - Useful for querying appointments for a specific doctor within a particular timeframe.

3. **Get First Available Appointment API:**
   - Enables patients to find the first available appointment after a specified time.
   - Useful for patients seeking immediate appointments.

#### Deployment Instructions:

To deploy the project to Google Cloud Platform (GCP), follow these steps:

1. Ensure you have a valid `project_id` set up in your GCP account.
2. Set up a Cloud SQL instance.
3. Run the following commands for deployment:
   ```
   gcloud builds submit --tag gcr.io/PROJECT-ID/opp_appointment
   gcloud run deploy --image gcr.io/PROJECT-ID/opp_appointment --platform managed
   ```
   Replace `PROJECT-ID` with your actual GCP project ID.

#### Notes:

- This system assumes a simple scheduling scenario with fixed working hours for each doctor.
- Further enhancements can include support for recurring appointments, notifications, and user authentication.
- Continuous testing and monitoring are recommended to ensure the reliability and scalability of the system.


## Running unit tests
All the tests can be run via ```pytest``` inside of the src/tests directory 
python -m pytest tests

## Running the full Project locally
python3 src/app.py
