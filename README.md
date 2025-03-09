
# **Appointment Scheduling System**

A robust system for scheduling appointments with two doctors, managing flexible appointment durations while respecting each doctor's working hours.

## **Features**

### **Models**
- **Appointment Model**:  
  - Handles appointments of variable lengths, ensuring scheduling flexibility.
  
- **Doctor Schedule Model**:  
  - **Doctor Strange**: Available **Monday to Friday, 9 AM - 5 PM**.  
  - **Doctor Who**: Available **Monday to Friday, 8 AM - 4 PM**.

### **APIs**
- **Create Appointment**:  
  - Books an appointment, ensuring no conflicts with existing appointments.  
  - Rejects requests if scheduling conflicts occur.  

- **Get Appointments Within Time Window**:  
  - Retrieves all appointments for a specific doctor within a specified timeframe.  

- **Get First Available Appointment**:  
  - Finds the earliest available slot after a specified time for a patient seeking an appointment.  

---

## **Deployment Instructions**
The system is deployed on **Google Cloud Platform (GCP)**.

### **Steps to Deploy**
1. Set up a **GCP project** and create a **Cloud SQL instance**.  
2. Deploy using the following commands:

   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/opp_appointment
   gcloud run deploy --image gcr.io/PROJECT-ID/opp_appointment --platform managed
   ```

   Replace `PROJECT-ID` with your actual **GCP project ID**.

---

## **Local Development**
### **Run the Project**
1. Navigate to the project directory.  
2. Start the application using:

   ```bash
   python3 src/app.py
   ```

### **Run Unit Tests**
Execute all tests using:

   ```bash
   python -m pytest tests
   ```

---

## **Notes & Future Enhancements**
- **Current limitations**: Fixed working hours for each doctor.  
- **Planned updates**:
  - Support for **recurring appointments**.  
  - Integration of a **notification system** (email/SMS reminders).  
  - Implementation of **user authentication and role-based access control**.  
  - **Monitoring system reliability and scalability** through continuous testing and optimization.  

---

