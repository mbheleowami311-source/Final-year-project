from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_cors import CORS
import secrets
import os
import requests
from datetime import date
import time as time_module
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError

patient = Flask(__name__)
patient.secret_key ="front_end_sk_change_later"

patient.config["SESSION_COOKIE_NAME"] = "clinic_portal_session"
patient.config["SESSION_COOKIE_HTTPONLY"] = True
patient.config["SESSION_COOKIE_SAMESITE"] = "Lax"
patient.config["SESSION_COOKIE_SECURE"] = False  # Local HTTP only
CORS(patient)

@patient.route("/")
def home():
    return render_template('landing_page.html')

@patient.route("/messages")
def messages():
    return render_template('messages.html')

@patient.route("/signin")
def login():
    message = request.args.get("message")
    print(message)
    flash(message, "danger")
    return render_template('login.html')

@patient.route("/signup")
def register():
    message=request.args.get("message")
    flash(message, "danger")
    return render_template('register.html')


@patient.route("/patientDashboard", methods=["GET"])
def patientDashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    today = date.today()

    selected_date = request.args.get(
        "selected_date", today.isoformat()
    )

    min_date = today.isoformat()

    current_year = request.args.get(
        "current_year", type=int
    ) or today.year

    message=request.args.get("message")
    flash(message, "success")

    available_slots = request.args.getlist("available_slots")

    return render_template(
        "patientDashboard.html",
        patient_name=session.get("name"),
        patient_email=session.get("email"),
        patient_id=session.get("patient_id"),
        selected_date=selected_date,
        min_date=min_date,
        current_year=current_year,
        available_slots=available_slots
    )

@patient.route("/rescheduleAppointments", methods=["GET"])
def rescheduleAppointments():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    today = date.today()

    selected_date = request.args.get(
        "selected_date", today.isoformat()
    )

    appointment_id = request.args.get(
        "appointment_id", type=int
    )

    available_slots = request.args.getlist("available_slots")

    # Keep your existing logic for fetching the patient's appointments.
    # It must assign the result to `appointments`.

    return render_template(
        "appointments.html",
        appointments=appointments,
        appointment_id=appointment_id,
        selected_date=selected_date,
        min_date=today.isoformat(),
        current_year=today.year,
        available_slots=available_slots,
        patient_name=session.get("name"),
        patient_email=session.get("email"),
        patient_id=session.get("patient_id")
    )
# @patient.route("/patientDashboard", methods= ["GET"])
# def patientDashboard():

#     patient_email = request.args.get("useremail")
    
#     session["email"] = patient_email
#     today = date.today()

#     selected_date = request.args.get(
#         "selected_date", today.isoformat()
#     )

#     min_date = request.args.get(
#         "min_date", today.isoformat()
#     )

#     current_year = request.args.get(
#         "current_year", type=int
#     ) or today.year

#     available_slots = request.args.getlist("available_slots")

#     print("Dashboard date:", selected_date)
#     print("Received available slots:", available_slots)

#     return render_template(
#         "patientDashboard.html",
#         selected_date=selected_date,
#         min_date=min_date,
#         current_year=current_year,
#         available_slots=available_slots
#     )

@patient.route("/auth/callback", methods=["GET"])
def auth_callback():
    code = request.args.get("code", "").strip()

    if not code:
        flash("invalid user name or password", "danger")
        return redirect(url_for("login"))

    # The frontend and backend must use the same secret key.
    api_key = "grhxhchxxfzfdv"

    if not api_key:
        patient.logger.error(
            "CLINIC_INTERNAL_API_KEY is not configured."
        )
        flash("invalid user name or password", "danger")
        return "Login configuration error. Please contact support.", 500

    try:
        response = requests.post(
            "http://127.0.0.1:8080/api/auth/exchange",
            json={"code": code},
            headers={
                "X-Internal-API-Key": api_key
            },
            timeout=5
        )

        if response.status_code != 200:
            patient.logger.warning(
                "Login code exchange failed: HTTP %s",
                response.status_code
            )
            flash("invalid user name or password", "danger")
            return redirect(url_for("login"))

        user = response.json()

        # Validate the returned patient data.
        required_fields = [
            "patient_id",
            "name",
            "email",
            "role"
        ]

        if not all(field in user for field in required_fields):
            patient.logger.error(
                "Backend returned incomplete patient data."
            )
            flash("invalid user name or password", "danger")
            return "Invalid login response from backend.", 502

    except (requests.RequestException, ValueError) as error:
        patient.logger.error(
            "Could not verify login with backend: %s", error
        )
        flash("invalid user name or password", "danger")
        return "Could not verify your login with the backend.", 502

    # Create the session in the port 5000 application.
    session.clear()
    session["user_id"] = user["patient_id"]
    session["patient_id"] = user["patient_id"]
    session["name"] = user["name"]
    session["email"] = user["email"]
    session["role"] = user["role"]
    session["logged_in"] = True

    # Redirect to your patient dashboard.
    return redirect(url_for("patientDashboard"))

@patient.route("/appointments", methods=["GET", "POST"])
def myappointments():


    # if request.method == "GET":
    #     return render_template("appointments.html")

    # Get the patient's email.
    # The email can be passed in the URL or stored in port 5000's session.
    email = (
        request.args.get("email")
        or session.get("email")
    )


    if not email:
        return "Patient email is missing", 400

    try:
        # Request the actual appointment records from port 8080.
        response = requests.get(
            "http://127.0.0.1:8080/api/my-appointments",
            params={"email": email}
            
        )

        response.raise_for_status()

        # Convert the API's JSON response into Python data.
        data = response.json()
        appointments = data.get("appointments", [])

        print("Appointments received:", appointments)

        # Send appointment objects to the template.
        return render_template(
            "appointments.html",
            appointments=appointments,
            min_date=date.today().isoformat(),
            available_slots_by_appointment={}
        )

    except requests.RequestException as error:
        print("Error contacting port 8080:", error)

        return "Unable to retrieve appointments from the clinic server.", 502




@patient.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__=="__main__":
    patient.run(debug=True)