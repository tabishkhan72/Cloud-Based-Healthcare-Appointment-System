# **🩺 Appointment Scheduling System**  

A robust and flexible **appointment scheduling system** for managing **doctor availability and patient bookings**. This system supports **variable appointment durations** while ensuring conflict-free scheduling within each doctor's working hours. 

---

## **🚀 Features**  

### **📌 Models**  
- **Appointment Model**  
  - Handles appointments of **variable lengths**, ensuring scheduling flexibility.  

- **Doctor Schedule Model**  
  - **Doctor Strange**: Available **Monday to Friday, 9 AM - 5 PM**  
  - **Doctor Who**: Available **Monday to Friday, 8 AM - 4 PM**  

---

### **🔗 API Endpoints**  

| **API**  | **Description** |
|----------|---------------|
| **`/api/appointments/create`**  | Books an appointment, ensuring no scheduling conflicts. |
| **`/api/appointments/time-window`**  | Retrieves all appointments for a doctor within a specific timeframe. |
| **`/api/appointments/first-available`**  | Finds the earliest available appointment slot for a patient. |

- **Conflict Prevention**: Ensures no double-booking or scheduling outside working hours.  
- **Optimized Availability Search**: Quickly identifies the next available appointment for patients.  

---

## **🌍 Deployment Instructions**  
The system is **deployed on Google Cloud Platform (GCP)** using **Cloud Run** and **Cloud SQL**.  

### **🚀 Steps to Deploy**  
1️⃣ Set up a **GCP project** and create a **Cloud SQL instance**  
2️⃣ Deploy using the following commands:  

```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/appointment-system
gcloud run deploy --image gcr.io/PROJECT-ID/appointment-system --platform managed
```

Replace **`PROJECT-ID`** with your **actual GCP project ID**  

---

## **🛠 Local Development**  

### **1️⃣ Run the Application**  
Ensure you have **Python 3.8+** installed. Start the application locally:  

```bash
python3 src/app.py
```

### **2️⃣ Run Unit Tests**  
Execute all unit tests using:  

```bash
python -m pytest tests
```

---

## **🚀 Future Enhancements**  

✅ **Recurring Appointments** – Allow patients to book recurring slots together  
✅ **Notification System** – Email/SMS reminders for upcoming appointments  
✅ **User Authentication** – Implement role-based access control  
✅ **Reliability & Scalability** – Continuous monitoring and optimization for system performance.  

