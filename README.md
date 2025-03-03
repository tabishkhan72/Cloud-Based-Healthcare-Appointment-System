Appointment Scheduling System
A robust system for scheduling appointments with two doctors, managing flexible appointment durations while respecting each doctor's working hours.

Features
Models:
Appointment Model:
Handles appointments of variable lengths.
Doctor Schedule Model:
Doctor Strange: 9 AM - 5 PM, Monday to Friday.
Doctor Who: 8 AM - 4 PM, Monday to Friday.
APIs:
Create Appointment:

Books an appointment, ensuring no conflicts with existing appointments.
Rejects requests if scheduling conflicts occur.
Get Appointments Within Time Window:

Retrieves all appointments for a specific doctor within a specified timeframe.
Get First Available Appointment:

Finds the earliest available slot after a specified time for a patient seeking an appointment.
Deployment Instructions
Deploy the system on Google Cloud Platform (GCP):

Set up a GCP project and create a Cloud SQL instance.
Deploy using the following commands:
bash
Copy code
gcloud builds submit --tag gcr.io/PROJECT-ID/opp_appointment
gcloud run deploy --image gcr.io/PROJECT-ID/opp_appointment --platform managed
Replace PROJECT-ID with your GCP project ID.
Local Development
Run the Project:
Navigate to the project directory.
Start the application:
bash
Copy code
python3 src/app.py
Run Unit Tests:
Execute all tests using:

bash
Copy code
python -m pytest tests
Notes & Future Enhancements
Fixed working hours for each doctor. Future updates may include:
Recurring appointments.
Notification systems.
User authentication.
Monitor system reliability and scalability through continuous testing.
