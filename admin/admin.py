from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import webbrowser
from datetime import date, time
from datetime import datetime, date
from sqlalchemy import Enum
from sqlalchemy.dialects.mysql import TIME
import mysql.connector
from flask_mysqldb import MySQL
from datetime import datetime


admin = Flask(__name__)
admin.secret_key = 'secret@21117'
admin.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/admin'
db = SQLAlchemy(admin)

class appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_license_number = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    dea_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Assistants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_license_number = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class finished(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

# Gmail SMTP Configuration---------------------
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'telehealth115@gmail.com'
SMTP_PASSWORD = 'osde cnun rafg jczr'


# send mails to patients and for doctors------------------------------
@admin.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        room_id = request.form['room_id']
        patient_emails = request.form.getlist('patient_email') 
        doctor_email = request.form['doctor_email']

# Retrieve appointment details based on the entered appointment ID for send emails-----------------------------------
        appointment = appointments.query.filter_by(id=appointment_id).first()

        if appointment:
            patient_message = f'Dear {appointment.first_name},\n\nYour appointment on {appointment.date} at {appointment.time} in room {room_id} has been confirmed.\n\nBest regards,\nYour Clinic'

            doctor_message = f'Dear Dr. {doctor_email},\n\nYou have an appointment with {appointment.first_name} on {appointment.date} at {appointment.time} in room {room_id}.\n\nBest regards,\nYour Clinic'

            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()  # TLS encryption
                server.login(SMTP_USERNAME, SMTP_PASSWORD)

                # Email to patient
                for patient_email in patient_emails:
                    patient_msg = MIMEMultipart()
                    patient_msg['From'] = SMTP_USERNAME
                    patient_msg['To'] = patient_email
                    patient_msg['Subject'] = 'Appointment Confirmation'
                    patient_msg.attach(MIMEText(patient_message, 'plain'))

                    server.sendmail(SMTP_USERNAME, patient_email, patient_msg.as_string())

                # Email to doctor
                doctor_msg = MIMEMultipart()
                doctor_msg['From'] = SMTP_USERNAME
                doctor_msg['To'] = doctor_email
                doctor_msg['Subject'] = 'Appointment Notification'
                doctor_msg.attach(MIMEText(doctor_message, 'plain'))

                server.sendmail(SMTP_USERNAME, doctor_email, doctor_msg.as_string())

                server.quit()

                return 'Emails sent successfully!'
            except Exception as e:
                return f'Error sending email: {str(e)}'
        else:
            return 'Appointment not found.'
        

# fetch doctors emails to send emails---------------------------------
@admin.route('/email')
def email_page():

    doctors = Doctor.query.all()
    emails = [doctor.email for doctor in doctors]
    return render_template('email.html', emails=emails)


 # Retrieve appointment details based on the provided appointment ID--------------------------------
@admin.route('/auto_fill_details')
def auto_fill_details():
    appointment_id = request.args.get('appointment_id')
   
    Appointment = appointments.query.filter_by(id=appointment_id).first()
    if Appointment:
        return jsonify({
            'nic_number': Appointment.nic_number,
            'first_name': Appointment.first_name,
            'last_name': Appointment.last_name,
            'gender': Appointment.gender,
            'age': Appointment.age,
            'telephone': Appointment.telephone,
            'email': Appointment.email,
            'date': str(Appointment.date),
            'time': str(Appointment.time)
        })
    else:
        return jsonify({'error': 'Appointment not found'}), 404 

#home route
@admin.route('/')
def base():
   
    return redirect(url_for('home'))


@admin.route('/home')
def home():
    # Check if user is logged in
    if 'email' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))



#fetch appointments details-------------------------------------------------
@admin.route('/appointments')
def get_appointments():
    Appointments = appointments.query.all()
    events = []
    for appointment in Appointments:
        event = {
            'id': appointment.id,
            'title': str(appointment.id),
            'start': appointment.date.strftime('%Y-%m-%d') + 'T' + appointment.time.strftime('%H:%M:%S'),
        }
        events.append(event)
    return jsonify(events)

@admin.route('/appointment/<int:appointment_id>')
def get_appointment_details(appointment_id):
    appointment = appointments.query.get(appointment_id)
    if appointment:
        appointment_details = {
            'id': appointment.id,
            'nic_number': appointment.nic_number,
            'first_name': appointment.first_name,
            'last_name': appointment.last_name,
            'gender': appointment.gender,
            'age': appointment.age,
            'telephone': appointment.telephone,
            'email': appointment.email,
            'date': appointment.date.strftime('%Y-%m-%d'),
            'time': appointment.time.strftime('%H:%M:%S')
        }
        return jsonify(appointment_details)
    else:
        return jsonify({'error': 'Appointment not found'}), 404
    
@admin.route('/appointment_form')
def appointment_form():
    doctors = Doctor.query.all()
    return render_template('email.html', doctors=doctors)


@admin.route('/email')
def email():
    return render_template('email.html')

@admin.route('/doctors')
def list_doctors():
    doctors_list = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors_list)

@admin.route('/assistants')
def list_assistants():
    assistants_list = Assistants.query.all()
    return render_template('assistants.html', assistants=assistants_list)

@admin.route('/consultation')
def consultation():
    return render_template('consultation.html')



#Add doctors------------------------------------------------
@admin.route('/add_doctor', methods=['POST'])
def add_doctor():
    medical_license_number = request.form['medical_license_number']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    gender = request.form['gender']
    contact_number = request.form['contact_number']
    email = request.form['email']
    specialty = request.form['specialty']
    dea_number = request.form['dea_number']
    password = request.form['password']

    
    new_doctor = Doctor(medical_license_number=medical_license_number, 
                        first_name=first_name, 
                        last_name=last_name, 
                        dob=dob, 
                        gender=gender, 
                        contact_number=contact_number, 
                        email=email, 
                        specialty=specialty, 
                        dea_number=dea_number,
                        password=password)
    
    db.session.add(new_doctor)
    db.session.commit()
    
    return redirect(url_for('list_doctors'))

#Update doctors--------------------------------------------------------
@admin.route('/update_doctor/<int:id>', methods=['GET', 'POST'])
def update_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    if request.method == 'POST':
        doctor.medical_license_number = request.form['medical_license_number']
        doctor.first_name = request.form['first_name']
        doctor.last_name = request.form['last_name']
        doctor.dob = request.form['dob']
        doctor.gender = request.form['gender']
        doctor.contact_number = request.form['contact_number']
        doctor.email = request.form['email']
        doctor.specialty = request.form['specialty']
        doctor.dea_number = request.form['dea_number']
        db.session.commit()
        flash('Doctor updated successfully', 'success')
        return redirect(url_for('list_doctors'))
    return render_template('update_doctor.html', doctor=doctor)


#delete doctors-------------------------------------------------
@admin.route('/delete_doctor', methods=['GET'])
def delete_doctor():
    id = request.args.get('id')
    if not id:
        flash('Doctor ID is required.', 'error')
        return redirect(url_for('list_doctors'))

    try:
        doctor = Doctor.query.get(id)
        if not doctor:
            flash('Doctor not found.', 'error')
            return redirect(url_for('list_doctors'))

        db.session.delete(doctor)
        db.session.commit()
        flash('Doctor deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting doctor: {str(e)}', 'error')

    return redirect(url_for('list_doctors'))


#Add medical assistants----------------------------------------------
@admin.route('/add_assistant', methods=['POST'])
def add_assistant():
    medical_license_number = request.form['medical_license_number']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    gender = request.form['gender']
    contact_number = request.form['contact_number']
    email = request.form['email']
    password = request.form['password']
    
    new_assistant = Assistants(medical_license_number=medical_license_number, 
                        first_name=first_name, 
                        last_name=last_name, 
                        dob=dob, 
                        gender=gender, 
                        contact_number=contact_number, 
                        email=email,
                        password=password)
    db.session.add(new_assistant)
    db.session.commit()
    
    return redirect(url_for('list_assistants'))



#Update assistants--------------------------------------------------
@admin.route('/update_assistant/<int:id>', methods=['GET', 'POST'])
def update_assistant(id):
    assistants = Assistants.query.get_or_404(id)
    if request.method == 'POST':
        assistants.medical_license_number = request.form['medical_license_number']
        assistants.first_name = request.form['first_name']
        assistants.last_name = request.form['last_name']
        assistants.dob = request.form['dob']
        assistants.gender = request.form['gender']
        assistants.contact_number = request.form['contact_number']
        assistants.email = request.form['email']
        db.session.commit()
        flash('Medical Assistant updated successfully', 'success')
        return redirect(url_for('list_assistants'))
    return render_template('update_assistant.html', assistants=assistants)

@admin.route('/delete_assistant', methods=['GET'])
def delete_assistant():
    id = request.args.get('id')
    if not id:
        flash('Assistant ID is required.', 'error')
        return redirect(url_for('list_assistants'))

   
    assistants = Assistants.query.get(id)
    if not Assistants:
            flash('Assistant not found.', 'error')
            return redirect(url_for('list_assistants'))

    db.session.delete(assistants)
    db.session.commit()
    flash('Assistant deleted successfully.', 'success')

    return redirect(url_for('list_assistants'))


class patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(255), index=True)
    password = db.Column(db.String(255))
    current_month = db.Column(db.String(255))


class cancelled(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    date = db.Column(db.Date)
    time = db.Column(db.Time)



# Route to provide total counts of all tables-----------------------
@admin.route('/get_counts')
def get_counts():
    # Retrieve counts from the database
    patients_count = patients.query.count()

    # Return counts as JSON
    return jsonify({'patient_count': patients_count})

from collections import Counter
from datetime import datetime


#get patient count per month------------------------------------
@admin.route('/patient_data')
def patient_data():
    # Query the database to get patient counts per month
    patients_data = patients.query.all()

    # Extract current month values
    months = [patient.current_month for patient in patients_data]

    # Count occurrences of each month
    month_counts = Counter(months)

    # Extracting months and their counts, sorted by month order
    sorted_months = sorted(month_counts.keys(), key=lambda month: datetime.strptime(month, "%B").strftime("%m"))


    # Calculate cumulative counts
    cumulative_counts = []
    total_count = 0
    for month in sorted_months:
        total_count += month_counts[month]
        cumulative_counts.append(total_count)

    # Return data as JSON
    return jsonify(months=sorted_months, counts=cumulative_counts)


#cancelled appointments count-----------------------------------------------------
@admin.route('/cancelled_counts')
def cancelled_counts():

    today = date.today()

    # Retrieve today cancel counts
    cancelled_count = cancelled.query.filter(cancelled.date == today).count()

    # Counts as JSON
    return jsonify({'cancelled_count': cancelled_count})


# Count of today's appointments
@admin.route('/today_appointments_count')
def today_appointments_count():
    today_appointments_count = appointments.query.filter_by(date=date.today()).count()

    return jsonify({'today_appointments_count': today_appointments_count})

# Count of today's finished appointments
@admin.route('/finished_appointments_count')
def finished_appointments_count():

    finished_appointments_count = finished.query.filter_by(date=date.today()).count()

    return jsonify({'finished_appointments_count': finished_appointments_count})


# Mark an appointment as finished and move it to the finished table
@admin.route('/mark_as_finished/<int:appointment_id>', methods=['POST'])
def mark_as_finished(appointment_id):
    try:
        appointment = appointments.query.get(appointment_id)
        if appointment:
            finished_appointment = finished(
                nic_number=appointment.nic_number,
                first_name=appointment.first_name,
                last_name=appointment.last_name,
                gender=appointment.gender,
                age=appointment.age,
                telephone=appointment.telephone,
                email=appointment.email,
                date=appointment.date,
                time=appointment.time
            )
            db.session.add(finished_appointment)
            db.session.commit()

            # Delete the appointment from the appointments table
            db.session.delete(appointment)
            db.session.commit()

            return jsonify({'message': 'Appointment marked as finished and moved to the finished table.'}), 200
        else:
            return jsonify({'error': 'Appointment not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#finished appointments---------------------------------------------

@admin.route('/get_finished_appointments')
def get_finished_appointments():
    finished_appointments = finished.query.filter_by(date=date.today()).all()

    appointments_list = []
    for appointment in finished_appointments:
        appointment_dict = {
            'id': appointment.id,
            'nic_number': appointment.nic_number,
            'first_name': appointment.first_name,
            'last_name': appointment.last_name,
            'gender': appointment.gender,
            'age': appointment.age,
            'telephone': appointment.telephone,
            'email': appointment.email,
            'time': str(appointment.time)
        }
        appointments_list.append(appointment_dict)

    return jsonify({'finished_appointments': appointments_list})



#Today cancelled appointments-----------------------------
@admin.route('/cancelled-appointments')
def cancelled_appointments():
    today = date.today()

    cancelled_records_today = cancelled.query.filter(cancelled.date == today).all()

    cancelled_count_today = len(cancelled_records_today)

    cancelled_data_today = [{
        'id': record.id,
        'nic_number': record.nic_number,
        'first_name': record.first_name,
        'last_name': record.last_name,
        'gender': record.gender,
        'age': record.age,
        'telephone': record.telephone,
        'email': record.email,
        'date': record.date.strftime('%Y-%m-%d'),
        'time': record.time.strftime('%H:%M:%S')
    } for record in cancelled_records_today]

    return jsonify(cancelled_count_today=cancelled_count_today, cancelled_data_today=cancelled_data_today)



# MySQL Configuration----------------------------
admin.config['MYSQL_HOST'] = 'localhost'
admin.config['MYSQL_USER'] = 'root'
admin.config['MYSQL_PASSWORD'] = ''
admin.config['MYSQL_DB'] = 'admin'

mysql = MySQL(admin)


# Login route------------------------------------
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the entered email and password already exist in the admin table
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
        admin = cur.fetchone()
        cur.close()

        if admin:
            session['email'] = email
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or medical license number. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')


#logout route---------------------------------------
@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':

        session.clear()

        return redirect(url_for('login'))

    return redirect(url_for('login'))


if __name__ == '__main__':
    admin.run(debug=True, port=5001)