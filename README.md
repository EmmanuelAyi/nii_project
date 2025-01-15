# **Nii's SPA USSD Booking Application**  

This is a USSD-based SPA appointment booking application built using Flask. The application supports appointment scheduling, contact management, and treatment selection through a USSD interface.  

---

## **Project Structure**  

```
flask_app/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models (SQLAlchemy)
│   ├── routes.py            # Route definitions and logic
│   ├── services.py          # Session management service
│   └── config.py            # App configuration (database settings)
├── migrations/              # Database migrations (if applicable)
├── venv/                    # Virtual environment (not included in the repo)
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # Project documentation (this file)
```

---

## **Features**  
1. **USSD Appointment Booking**:  
   - Check available days  
   - Book an appointment  
   - Cancel the session  

2. **Data Storage**:  
   - SQLite Database Integration  
   - Appointment details stored securely  

3. **Session Management**:  
   - In-memory session management using a custom session class  

4. **Modular Code Structure**:  
   - Flask Blueprints for cleaner code organization  

---

## **Testing the USSD App with Ngrok**  

1. Start the Flask app:  
   ```
   python run.py
   ```

2. Start Ngrok:  
   ```
   ngrok http 5000
   ```

3. Use the Ngrok URL in your USSD simulator[postman] or provider configuration[Nalo].  

---

## **Usage Guide**  

### USSD Flow Breakdown:  
- **Welcome Screen**: Choose options (Check available days, Book, or Cancel)  
- **Appointment Day Selection**: Select a day or go back  
- **Contact Information**: Enter a contact number or return to the previous menu  
- **Treatment Selection**: Choose a preferred treatment or cancel the session  

---

## **Dependencies**  
- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- Gunicorn (for deployment)  

---

## **Author**  
- **Nii Ayi's SPA Project Team**  
- **Contact Email**: eayi-bonte@nalosolutions.com  

