from flask import Flask, render_template, jsonify, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root1234',
    'database': 'dseu'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return None

def get_available_courses():
    try:
        connection = get_db_connection()
        if not connection:
            return []
        
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        courses = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        return courses
    except Exception as e:
        logger.error(f"Error getting courses: {str(e)}")
        return []

def get_semesters(course):
    try:
        connection = get_db_connection()
        if not connection:
            return []
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT DISTINCT semester FROM {course} ORDER BY semester")
        semesters = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        return semesters
    except Exception as e:
        logger.error(f"Error getting semesters: {str(e)}")
        return []

def get_subjects(course, semester):
    try:
        connection = get_db_connection()
        if not connection:
            return []
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT subject FROM {course} WHERE semester = %s ORDER BY subject", (semester,))
        subjects = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        return subjects
    except Exception as e:
        logger.error(f"Error getting subjects: {str(e)}")
        return []

def get_subject_details(course, semester, subject):
    try:
        connection = get_db_connection()
        if not connection:
            return {'syllabus': '', 'notes': ''}
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"""
            SELECT syllabus, notes 
            FROM {course} 
            WHERE semester = %s AND subject = %s
        """, (semester, subject))
        
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            return {
                'syllabus': result['syllabus'],
                'notes': result['notes']
            }
        return {'syllabus': '', 'notes': ''}
    except Exception as e:
        logger.error(f"Error getting subject details: {str(e)}")
        return {'syllabus': '', 'notes': ''}

@app.route('/')
def index():
    courses = get_available_courses()
    return render_template('index.html', courses=courses)

@app.route('/get_semesters/<course>')
def fetch_semesters(course):
    semesters = get_semesters(course)
    return jsonify(semesters)

@app.route('/get_subjects/<course>/<semester>')
def fetch_subjects(course, semester):
    subjects = get_subjects(course, semester)
    return jsonify(subjects)

@app.route('/get_details/<course>/<semester>/<subject>')
def fetch_details(course, semester, subject):
    details = get_subject_details(course, semester, subject)
    return jsonify(details)

@app.route('/send_contact', methods=['POST'])
def send_contact():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = 'aayushmish18@gmail.com'  # Changed from email to your email
        msg['To'] = 'aayushmish18@gmail.com'
        msg['Subject'] = f'Course Request from {name}'
        
        body = f"""
        Name: {name}
        Email: {email}
        Request: {message}
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('aayushmish18@gmail.com', 'xyzz abcd efgh ijkl')  # Replace with your app password
        text = msg.as_string()
        server.sendmail('aayushmish18@gmail.com', 'aayushmish18@gmail.com', text)
        server.quit()
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error sending contact email: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)