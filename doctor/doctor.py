from flask import Flask, render_template, redirect, url_for, jsonify, request, send_from_directory, session, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
from datetime import datetime
import smtplib
import mysql.connector
from flask_mysqldb import MySQL
import pymysql.cursors
from collections import Counter

doctor = Flask(__name__)
doctor.secret_key = 'doctor@21117'



# Configure database
doctor.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ecg'
doctor.config['SQLALCHEMY_BINDS'] = {'admin': 'mysql://root:@localhost/admin'}
doctor.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(doctor)


# MySQL Configuration
doctor.config['MYSQL_HOST'] = 'localhost'
doctor.config['MYSQL_USER'] = 'root'
doctor.config['MYSQL_PASSWORD'] = ''
doctor.config['MYSQL_DB'] = 'admin'

mysql = MySQL(doctor)


@doctor.route('/prescription')
def add_prescriptions():
    return render_template('prescription.html')

@doctor.route('/consultation')
def online_consultations():
    return render_template('consultation.html')


# display patients records-------------------------------------------
@doctor.route('/records')
def display_records():
    normal_records = normal.query.all()
    arrhythmia_records = arrhythmia.query.all()
    myocardial_infarction_records = myocardial_infarction.query.all()
    history_of_mi_records = history_of_mi.query.all()
    
    return render_template('records.html', normal_records=normal_records, arrhythmia_records=arrhythmia_records, 
                           myocardial_infarction_records=myocardial_infarction_records, history_of_mi_records=history_of_mi_records)



# total counts---------------------------------------------------
@doctor.route('/get_counts')
def get_counts():
    normal_count = normal.query.count()
    arrhythmia_count = arrhythmia.query.count()
    history_of_mi_count = history_of_mi.query.count()
    myocardial_infarction_count = myocardial_infarction.query.count()

    total_count = normal_count + arrhythmia_count + history_of_mi_count + myocardial_infarction_count

    return jsonify({'product_count': total_count})

class normal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(20))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    image_path = db.Column(db.String(255))
    image_name = db.Column(db.String(255))
    prediction = db.Column(db.String(50))
    prediction_time = db.Column(db.DateTime)

class arrhythmia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(20))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    image_path = db.Column(db.String(255))
    image_name = db.Column(db.String(255))
    prediction = db.Column(db.String(50))
    prediction_time = db.Column(db.DateTime)

class myocardial_infarction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(20))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    image_path = db.Column(db.String(255))
    image_name = db.Column(db.String(255))
    prediction = db.Column(db.String(50))
    prediction_time = db.Column(db.DateTime)

class history_of_mi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(20))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    image_path = db.Column(db.String(255))
    image_name = db.Column(db.String(255))
    prediction = db.Column(db.String(50))
    prediction_time = db.Column(db.DateTime)

class Doctor(db.Model):
    __bind_key__ = 'admin'
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    medical_license_number = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(255))
    specialty = db.Column(db.String(255))
    dea_number = db.Column(db.String(255))
    password = db.Column(db.String(50))

def get_db_connection():
    return mysql.connection


# add prescription --------------------------------------------------------
@doctor.route('/add_prescription', methods=['POST'])
def add_prescription_submit():
    if request.method == 'POST':
     nic_number = request.form.get('nic_number', None)
    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    gender = request.form.get('gender', None)
    age = request.form.get('age', None)
    telephone = request.form.get('telephone', None)
    email = request.form.get('email', None)
    medication1 = request.form.get('medication1', default="")
    dosage1 = request.form.get('dosage1', default="")
    times1M = request.form.get('times1M', default="")
    times1A = request.form.get('times1A', default="")
    times1N = request.form.get('times1N', default="")
    medication2 = request.form.get('medication2', default="")
    dosage2 = request.form.get('dosage2', default="")
    times2M = request.form.get('times2M', default="")
    times2A = request.form.get('times2A', default="")
    times2N = request.form.get('times2N', default="")
    medication3 = request.form.get('medication3', default="")
    dosage3 = request.form.get('dosage3', default="")
    times3M = request.form.get('times3M', default="")
    times3A = request.form.get('times3A', default="")
    times3N = request.form.get('times3N',default="")
    medication4 = request.form.get('medication4', default="")
    dosage4 = request.form.get('dosage4', default="")
    times4M = request.form.get('times4M', default="")
    times4A = request.form.get('times4A', default="")
    times4N = request.form.get('times4N', default="")
    additional = request.form.get('additional', default="")
    lifestyle = request.form.get('lifestyle', default="")
    emergency = request.form.get('emergency', default="")
    doc_name = request.form.get('doc_name', None)
    date = request.form.get('date', None)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO feedback (nic_number, first_name, last_name, gender, age, telephone, email, date, medication1, dosage1, times1M, times1A, times1N, medication2, dosage2, times2M, times2A, times2N, medication3, dosage3, times3M, times3A, times3N, medication4, dosage4, times4M, times4A, times4N, additional, lifestyle, emergency, doc_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
               (nic_number, first_name, last_name, gender, age, telephone, email, date, medication1, dosage1, times1M, times1A, times1N, medication2, dosage2, times2M, times2A, times2N, medication3, dosage3, times3M, times3A, times3N, medication4, dosage4, times4M, times4A, times4N, additional, lifestyle, emergency, doc_name))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))



def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='admin',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

#fetch patient details to insert prescription-------------------------------------------
@doctor.route('/fetch_patient_details', methods=['GET'])
def fetch_patient_details():
    nic_number = request.args.get('nic_number')
    
    connection = get_db_connection()

    with connection.cursor() as cursor:
        sql = 'SELECT * FROM patients WHERE nic_number = %s'
        cursor.execute(sql, (nic_number,))
        patient_details = cursor.fetchone()

    connection.close()

    if patient_details:
        return jsonify(patient_details)
    else:
        return jsonify({'error': 'Patient not found'}), 404



#login route-------------------------------------------------------------------
@doctor.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM doctor WHERE email = %s AND password = %s", (email, password))
        doctor = cur.fetchone()
        cur.close()

        if doctor:
            session['email'] = email
            session['first_name'] = doctor[2] 
            return redirect(url_for('index'))
        else:
            error = 'Invalid email or medical license number. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')


#logout route--------------------------------------------------
@doctor.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return redirect(url_for('login'))



#fetch profile details-------------------------------------------
@doctor.route('/profile')
def profile():
    if 'email' not in session:
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('login'))

    email = session['email']
    doctor = Doctor.query.filter_by(email=email).first()

    if not doctor:
        flash('User not found.', 'error')
        return redirect(url_for('home')) 

    return render_template('profile.html', doctor=doctor)


#update password-------------------------------------------
@doctor.route('/update_password', methods=['POST'])
def update_password():
    new_password = request.form.get('new_password')
    
    doctor = Doctor.query.filter_by(email=session['email']).first()
    if doctor:
        doctor.password = new_password
        db.session.commit()
        flash('Password updated successfully.', 'success')
    else:
        flash('Doctor not found.', 'error')
    
    return redirect(url_for('profile'))


#prescription db-----------------------------------------------------
class feedback(db.Model):
    __bind_key__ = 'admin'
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(20))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    date = db.Column(db.Date)
    medication1 = db.Column(db.String(255))
    dosage1 = db.Column(db.Integer)
    times1M = db.Column(db.String(50))
    times1A = db.Column(db.String(50))
    times1N = db.Column(db.String(50))
    medication2 = db.Column(db.String(255))
    dosage2 = db.Column(db.Integer)
    times2M = db.Column(db.String(50))
    times2A = db.Column(db.String(50))
    times2N = db.Column(db.String(50))
    medication3 = db.Column(db.String(255))
    dosage3 = db.Column(db.Integer)
    times3M = db.Column(db.String(50))
    times3A = db.Column(db.String(50))
    times3N = db.Column(db.String(50))
    medication4 = db.Column(db.String(255))
    dosage4 = db.Column(db.Integer)
    times4M = db.Column(db.String(50))
    times4A = db.Column(db.String(50))
    times4N = db.Column(db.String(50))
    additional = db.Column(db.String(255))
    lifestyle = db.Column(db.String(255))
    emergency = db.Column(db.String(255))
    doc_name = db.Column(db.String(255))


# route to retrieve prescription based on nic_number------------------------------------
@doctor.route('/feedback/<nic_number>')
def get_feedback_by_nic_number(nic_number):
    feedback_data = feedback.query.filter_by(nic_number=nic_number).all()

    data_by_date = {}

    for entry in feedback_data:
        date_str = str(entry.date)
        if date_str not in data_by_date:
            data_by_date[date_str] = []
        data_by_date[date_str].append({
            'first_name': entry.first_name,
            'last_name': entry.last_name,
            'gender': entry.gender,
            'age': entry.age,
            'telephone': entry.telephone,
            'email': entry.email,
            'medication1': entry.medication1,
            'dosage1': entry.dosage1,
            'times1M': entry.times1M,
            'times1A': entry.times1A,
            'times1N': entry.times1N,
            'medication2': entry.medication2,
            'dosage2': entry.dosage2,
            'times2M': entry.times2M,
            'times2A': entry.times2A,
            'times2N': entry.times2N,
            'medication3': entry.medication3,
            'dosage3': entry.dosage3,
            'times3M': entry.times3M,
            'times3A': entry.times3A,
            'times3N': entry.times3N,
            'additional': entry.additional,
        })

    return jsonify(data_by_date)


#index route-------------------------------------
@doctor.route('/index')
def index():
    if 'email' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    doctor.run(debug=True, port=5003)
