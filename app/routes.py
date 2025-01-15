from flask import Blueprint, request, jsonify
from .models import Appointment, db
from .services import Session

main = Blueprint('main', __name__)

# Available days and spa treatments
available_days = ['Monday', 'Wednesday', 'Friday']
treatments = {
    '1': {'name': 'Massages', 'price': 100.00},
    '2': {'name': 'Facials', 'price': 80.00},
    '3': {'name': 'Body Treat', 'price': 120.00},
    '4': {'name': 'Hair Rem/Chemical Peel', 'price': 150.00},
    '5': {'name': 'Mani/Pedicure', 'price': 50.00}
}

@main.route('/niiayispa', methods=['POST'])
def ussd():
    user_id = request.json.get("USERID", "")
    msisdn = request.json.get("MSISDN", "")
    user_data = request.json.get("USERDATA", "").strip()
    session_id = request.json.get("SESSIONID", "")

    # Check if SESSIONID is present
    if not session_id:
        return jsonify({"error": "SESSIONID is missing"}), 400

    # Initialize session
    session = Session(session_id)

    # Prepare response structure
    response = {
        "USERID": user_id,
        "MSISDN": msisdn,
        "SESSIONID": session_id,
        "MSGTYPE": True,  # Default to expecting input
        "MSG": "",  # This will hold the message to show to the user
    }

    # Stage 0: Welcome screen
    if session.get('stage') == '0':
        response['MSG'] = ("Welcome to Nii's SPA.\nKindly follow through to book an appointment with us:\n"
                           "1. Check available days\n2. Book Appointment\n3. Cancel")
        session.set('stage', '1')

    # Stage 1: Check available days or Book Appointment
    elif session.get('stage') == '1':
        if user_data == '1':  # User selects to check available days
            response['MSG'] = "Dear Client, we're available this week on Monday, Wednesday, and Friday for your bookings.\nPress 0 to go back."
        elif user_data == '2':  # User selects to book an appointment
            response['MSG'] = "Please select a day for your appointment:\n"
            for i, day in enumerate(available_days, 1):
                response['MSG'] += f"{i}. {day}\n"
            response['MSG'] += "4. Cancel\n0. Go Back"
            session.set('stage', '2')
        elif user_data == '3':  # User selects to cancel the session
            response['MSG'] = "Your session has been cancelled. Thank you!"
            response['MSGTYPE'] = False  # End the session
            session.clear()
        else:  # Invalid input
            response['MSG'] = ("Welcome to Nii's SPA.\nKindly follow through to book an appointment with us:\n"
                                "1. Check available days\n2. Book Appointment\n3. Cancel")

    # Stage 2: User selects day for booking
    elif session.get('stage') == '2':
        if user_data == '0':  # User goes back to previous stage
            response['MSG'] = ("Welcome to Nii's SPA.\nKindly follow through to book an appointment with us:\n"
                               "1. Check available days\n2. Book Appointment\n3. Cancel")
            session.set('stage', '1')
        else:
            try:
                day_choice = int(user_data) - 1
                if 0 <= day_choice < len(available_days):  # Valid day selection
                    session.set('day', available_days[day_choice])
                    response['MSG'] = f"Your appointment is scheduled for {available_days[day_choice]}.\nKindly enter your contact number:\n0. Go Back"
                    session.set('stage', '3')
                elif user_data == '4':  # User cancels the booking process
                    response['MSG'] = "Booking process cancelled."
                    response['MSGTYPE'] = False  # End the session
                    session.clear()
                else:  # Invalid day selection
                    response['MSG'] = "Invalid day selection. Please try again."
            except ValueError:  # Invalid input format
                response['MSG'] = "Invalid input. Please select a day."

    # Stage 3: User enters contact number
    elif session.get('stage') == '3':
        if user_data == '0':  # User goes back to select a day
            response['MSG'] = "Please select a day for your appointment:\n"
            for i, day in enumerate(available_days, 1):
                response['MSG'] += f"{i}. {day}\n"
            response['MSG'] += "4. Cancel\n0. Go Back"
            session.set('stage', '2')
        else:  # User enters contact number
            session.set('contact', user_data)
            response['MSG'] = "Choose your preferred spa treatment:\n"
            for key, treatment in treatments.items():
                response['MSG'] += f"{key}. {treatment['name']} - GHC {treatment['price']:.2f}\n"
            response['MSG'] += "0. Go Back"
            session.set('stage', '4')

    # Stage 4: User selects treatment
    elif session.get('stage') == '4':
        if user_data == '0':  # User goes back to previous stage
            response['MSG'] = f"Your appointment is scheduled for {session.get('day')}.\nKindly enter your contact number:\n0. Go Back"
            session.set('stage', '3')
        elif user_data in treatments:  # Valid treatment selection
            selected_treatment = treatments[user_data]
            session.set('treatment', selected_treatment['name'])
            session.set('price', selected_treatment['price'])
            # Save appointment details to database
            appointment = Appointment(
                day=session.get('day'),
                contact=session.get('contact'),
                treatment=selected_treatment['name'],
                price=selected_treatment['price']
            )
            db.session.add(appointment)
            db.session.commit()

            response['MSG'] = (f"Your appointment for {selected_treatment['name']} on {session.get('day')} is confirmed!\n"
                               f"Total bill: GHC {selected_treatment['price']:.2f}\n"
                               f"We will contact you at {session.get('contact')}. Thank you!")
            response['MSGTYPE'] = False  # End the session
            session.clear()
        else:  # Invalid treatment selection
            response['MSG'] = "Invalid treatment selection. Please choose a valid treatment option."

    # Return the JSON response
    return jsonify(response)
