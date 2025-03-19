from flask import Flask, render_template, jsonify, request
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Path to data files
DATA_DIR = '/Users/macbook/Documents/Minor Project/data'

def read_course_data(course):
    try:
        file_path = os.path.join(DATA_DIR, f'{course}.json')
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading course data: {str(e)}")
        return []

def get_available_courses():
    try:
        # Get available JSON files (without extension)
        courses = [f.split('.')[0] for f in os.listdir(DATA_DIR) if f.endswith('.json')]
        return courses
    except Exception as e:
        logger.error(f"Error getting courses: {str(e)}")
        return []

def get_semesters(course):
    try:
        course_data = read_course_data(course)
        semesters = sorted(set(item['semester'] for item in course_data))
        return semesters
    except Exception as e:
        logger.error(f"Error getting semesters: {str(e)}")
        return []

def get_subjects(course, semester):
    try:
        course_data = read_course_data(course)
        subjects = [item['subject'] for item in course_data if item['semester'] == int(semester)]
        return sorted(subjects)
    except Exception as e:
        logger.error(f"Error getting subjects: {str(e)}")
        return []

def get_subject_details(course, semester, subject):
    try:
        course_data = read_course_data(course)
        for item in course_data:
            if item['semester'] == int(semester) and item['subject'] == subject:
                return {
                    'syllabus': item.get('syllabus', ''),
                    'notes': item.get('notes', '')
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