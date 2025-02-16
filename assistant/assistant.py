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

assistant = Flask(__name__)
assistant.secret_key = 'assistant@21117'

UPLOAD_FOLDER = 'uploads'
assistant.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# Configure database
assistant.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ecg'
assistant.config['SQLALCHEMY_BINDS'] = {'admin': 'mysql://root:@localhost/admin'}
assistant.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(assistant)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Load Keras model
model = tf.keras.models.load_model('keras_model.h5')

# Load class labels
with open('labels.txt', 'r') as file:
    class_labels = file.read().splitlines()



#routes----------------------------------------------

@assistant.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@assistant.route('/')
def base():
    return redirect(url_for('home'))


@assistant.route('/predictions')
def predictions():
    return render_template('predictions.html')

@assistant.route('/patients')
def patients_page():
    patients_data = patients.query.all()  # Retrieve patients data from the ecg database
    return render_template('patients.html', patients_data=patients_data)



# Bind the assistants database
class assistants(db.Model):
    __bind_key__ = 'admin'  
    __tablename__ = 'assistants'
    id = db.Column(db.Integer, primary_key=True)
    medical_license_number = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(255))
    password = db.Column(db.String(50))



# assistant profile----------------------------------------------
@assistant.route('/profile')
def profile():
    # Check if the assistant is logged in
    if 'email' not in session:
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('login'))

    # Retrieve assistant details from the database based on the logged-in assistant's email
    email = session['email']
    assistant = assistants.query.filter_by(email=email).first()

    if not assistant:
        flash('User not found.', 'error')
        return redirect(url_for('home'))

    return render_template('profile.html', assistant=assistant)



# update password--------------------------------------------------
@assistant.route('/update_password', methods=['POST'])
def update_password():
    new_password = request.form.get('new_password')
    
    # Retrieved the assistant object based on the logged-in assitant
    assistant = assistants.query.filter_by(email=session['email']).first()
    if assistant:
        assistant.password = new_password
        db.session.commit()
        flash('Password updated successfully.', 'success')
    else:
        flash('Assistant not found.', 'error')
    
    return redirect(url_for('profile'))



# total counts of all tables------------------------------------
@assistant.route('/get_counts')
def get_counts():
    normal_count = normal.query.count()
    arrhythmia_count = arrhythmia.query.count()
    history_of_mi_count = history_of_mi.query.count()
    myocardial_infarction_count = myocardial_infarction.query.count()

    total_count = normal_count + arrhythmia_count + history_of_mi_count + myocardial_infarction_count

    # counts as JSON
    return jsonify({'product_count': total_count})


# db models--------------------------------------------------------------
class patients(db.Model):
    __bind_key__ = 'admin'
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    nic_number = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

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


# display records-----------------------------------------
@assistant.route('/records')
def display_records():
    normal_records = normal.query.all()
    arrhythmia_records = arrhythmia.query.all()
    myocardial_infarction_records = myocardial_infarction.query.all()
    history_of_mi_records = history_of_mi.query.all()
    
    return render_template('records.html', normal_records=normal_records, arrhythmia_records=arrhythmia_records, 
                           myocardial_infarction_records=myocardial_infarction_records, history_of_mi_records=history_of_mi_records)



 #Function to check ifimage file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# prediction route----------------------------------------
@assistant.route('/predictions', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('predictions.html', prediction="No file uploaded")
        
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('static', 'uploads', filename)
            file.save(filepath)
            
            prediction = predict_image(filepath)

            # retrive data from the form
            nic_number = request.form.get('nic_number')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            gender = request.form.get('gender')
            age = request.form.get('age')

            if prediction == "normal":
               new_entry = normal(nic_number=nic_number, first_name=first_name, last_name=last_name, gender=gender, age=age, image_path=filepath, image_name=filename, prediction=prediction, prediction_time=datetime.now())
            elif prediction == "arrhythmia":
               new_entry = arrhythmia(nic_number=nic_number, first_name=first_name, last_name=last_name, gender=gender, age=age, image_path=filepath, image_name=filename, prediction=prediction, prediction_time=datetime.now())
            elif prediction == "myocardial infarction":
               new_entry = myocardial_infarction(nic_number=nic_number, first_name=first_name, last_name=last_name, gender=gender, age=age, image_path=filepath, image_name=filename, prediction=prediction, prediction_time=datetime.now())
            else:
               new_entry = history_of_mi(nic_number=nic_number, first_name=first_name, last_name=last_name, gender=gender, age=age, image_path=filepath, image_name=filename, prediction=prediction, prediction_time=datetime.now())

            db.session.add(new_entry)
            db.session.commit()

            return render_template('predictions.html', filename=filename, prediction=prediction, nic_number=nic_number, first_name=first_name, last_name=last_name, gender=gender, age=age, image_path=filepath, prediction_time=new_entry.prediction_time.strftime('%Y-%m-%d %H:%M:%S'))

        
    return render_template('predictions.html')



# preprocess the image for prediction -------------------------------------
def preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    return img_array


# Function to make prediction------------------------------
def predict_image(image_path):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    return class_labels[predicted_class]


# display bar chart---------------------
@assistant.route('/bar_chart')
def bar_chart():
    return render_template('bar_chart.html')




# filter total count by date range in graph------------------------------------
@assistant.route('/get_data')
def get_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    normal_count = normal.query.filter(normal.prediction_time >= start_date, normal.prediction_time <= end_date).count()
    arrhythmia_count = arrhythmia.query.filter(arrhythmia.prediction_time >= start_date, arrhythmia.prediction_time <= end_date).count()
    myocardial_infarction_count = myocardial_infarction.query.filter(myocardial_infarction.prediction_time >= start_date, myocardial_infarction.prediction_time <= end_date).count()

    counts = {
        'Normal': normal_count,
        'Arrhythmia': arrhythmia_count,
        'Myocardial Infarction': myocardial_infarction_count
    }

    return jsonify(counts)


# display total count in number--------------------------
@assistant.route('/get_total_count')
def get_total_count():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    total_count = (
        normal.query.filter(normal.prediction_time >= start_date, normal.prediction_time <= end_date).count() +
        arrhythmia.query.filter(arrhythmia.prediction_time >= start_date, arrhythmia.prediction_time <= end_date).count() +
        myocardial_infarction.query.filter(myocardial_infarction.prediction_time >= start_date, myocardial_infarction.prediction_time <= end_date).count()
    )

    return jsonify(total_count)




#Gender Chart--------------------------------
def get_gender_counts():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='ecg'
    )
    cursor = conn.cursor()
    
    counts = {
        "normal": {"male": 0, "female": 0},
        "history_of_mi": {"male": 0, "female": 0},
        "arrhythmia": {"male": 0, "female": 0},
        "myocardial_infarction": {"male": 0, "female": 0}
    }
    
    for category in counts.keys():
        cursor.execute(f"SELECT gender, COUNT(*) FROM {category} GROUP BY gender")
        rows = cursor.fetchall()
        for row in rows:
            gender, count = row
            if gender is not None:
                counts[category][gender.lower()] = count
    
    conn.close()
    return counts



# pie chart for gender--------------------------------
@assistant.route('/data')
def chart_data():
    counts = get_gender_counts()
    categories = ["normal",  "arrhythmia", "myocardial_infarction"]
    data = {
        "categories": categories,
        "male_counts": [counts[category]["male"] for category in categories],
        "female_counts": [counts[category]["female"] for category in categories]
    }
    return jsonify(data)


#Age distribution------------------------------------------

def get_age_distribution():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='ecg'
    )
    cursor = conn.cursor()

    age_ranges = ["00-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-100"]
    age_counts = {}

    for table_name in ["arrhythmia", "normal", "myocardial_infarction"]:
        age_counts[table_name] = [0] * len(age_ranges)

        for i, age_range in enumerate(age_ranges):
            start_age, end_age = map(int, age_range.split('-'))
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE age BETWEEN {start_age} AND {end_age}")
            age_counts[table_name][i] = cursor.fetchone()[0]

    conn.close()
    return age_ranges, age_counts


# age distribution route --------------------------------------
@assistant.route('/age_distribution')
def age_distribution():
    age_ranges, age_counts = get_age_distribution()
    return jsonify({'age_ranges': age_ranges, 'age_counts': age_counts})

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'admin'
}

# fetch patient details----------------------------
@assistant.route('/fetch_patient_details', methods=['POST'])
def fetch_patient_details():
    data = request.json
    nic_number = data.get('nic_number')
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        cursor.execute("SELECT first_name, last_name, gender, age FROM patients WHERE nic_number = %s", (nic_number,))
        patient_details = cursor.fetchone()
    except Exception as e:
        print("Error fetching patient details:", e)
        patient_details = None
    finally:
        cursor.close()
        conn.close()
    
    return jsonify(patient_details)

@assistant.route('/view_image/<filename>')
def view_image(filename):
    return send_from_directory('static/uploads', filename)



# MySQL Configuration for admin database----------------------
assistant.config['MYSQL_HOST'] = 'localhost'
assistant.config['MYSQL_USER'] = 'root'
assistant.config['MYSQL_PASSWORD'] = ''
assistant.config['MYSQL_DB'] = 'admin'

mysql = MySQL(assistant)


# login route------------------------

@assistant.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM assistants WHERE email = %s AND password = %s", (email, password))
        assistants = cur.fetchone()
        cur.close()

        if assistants:
            # Store user info in session
            session['email'] = email
            session['first_name'] = assistants[2]
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')



# logout route---------------------------------------

@assistant.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return redirect(url_for('login'))



#Patient registration-----------------------------
@assistant.route('/add_patient', methods=['POST'])
def add_patient():
    nic_number = request.form['nic_number']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    age = request.form['age']
    telephone = request.form['telephone']
    email = request.form['email']
    password = request.form['password']

    # Check if the email already exists in the database
    existing_patient = patients.query.filter_by(email=email).first()
    if existing_patient:
        flash('Email already exists.', 'error')
        return redirect(url_for('list_patients'))

    try:
        new_patient = patients(nic_number=nic_number, 
                               first_name=first_name, 
                               last_name=last_name, 
                               gender=gender, 
                               age=age, 
                               telephone=telephone, 
                               email=email, 
                               password=password)
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient added successfully.', 'success')
    except Exception as e:
        flash(f'Error adding patient: {str(e)}', 'error')

    return redirect(url_for('list_patients'))


#delete patients---------------------------------

@assistant.route('/delete_patient', methods=['GET'])
def delete_patient():
    id = request.args.get('id')
    if not id:
        flash('Patient ID is required.', 'error')
        return redirect(url_for('list_patients'))

    try:
        patient = patients.query.get(id)
        if not patient:
            flash('Patient not found.', 'error')
            return redirect(url_for('list_patients'))

        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting patient: {str(e)}', 'error')

    return redirect(url_for('list_patients'))


if __name__ == '__main__':
    assistant.run(debug=True, port=5002)
