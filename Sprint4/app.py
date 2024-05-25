# app.py
from flask import Flask, json, render_template, request, redirect, url_for, flash, send_file, jsonify
import os
import shutil
import subprocess

# Make sure to install Flask
app = Flask(__name__)

# Necessary files and folders
UPLOAD_COURSE_FOLDER = 'uploaded_files/uploaded_course_files'
app.config['UPLOAD_COURSE_FOLDER'] = UPLOAD_COURSE_FOLDER

UPLOAD_CLASSROOM_FOLDER = 'uploaded_files/uploaded_classroom_files'
app.config['UPLOAD_CLASSROOM_FOLDER'] = UPLOAD_CLASSROOM_FOLDER

OUTPUT_FOLDER = 'generated_files'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Secret key for flash messages
app.config['SECRET_KEY'] = 'your_secret_key'

# Main page route
@app.route('/')
def index():
    return render_template('html/index.html') 

# Upload page route
@app.route('/uploadPage')
def upload_page_view():
    return render_template('html/uploadPage.html') 

# Schedule page route
@app.route('/schedulePage')
def schedule_page_view():
    return render_template('html/schedulePage.html')  

# Contact page route
@app.route('/contactPage')
def contact_page_view():
    return render_template('html/contactPage.html')  


# Course files upload route
@app.route('/uploadCourse', methods=['POST'])
def upload_course_files():
    full_path = app.config['UPLOAD_COURSE_FOLDER']
    if os.path.exists(full_path):
        shutil.rmtree(full_path)  # Delete the folder
    os.makedirs(full_path)  # Create the folder again

    # Save the files
    files = request.files
    for filename, file in files.items():
        if file and file.filename:
            file_path = os.path.join(full_path, file.filename)
            file.save(file_path)
            flash(f"File '{file.filename}' uploaded successfully.", 'success')
    
    return redirect(url_for('upload_page_view'))


# Classroom files upload route
@app.route('/uploadClassroom', methods=['POST'])
def upload_classroom_files():
    full_path = app.config['UPLOAD_CLASSROOM_FOLDER']
    if os.path.exists(full_path):
        shutil.rmtree(full_path)  # Delete the folder
    os.makedirs(full_path) # Create the folder again

    # Save the files
    files = request.files
    for filename, file in files.items():
        if file and file.filename:
            file_path = os.path.join(full_path, file.filename)
            file.save(file_path)
            flash(f"File '{file.filename}' uploaded successfully.", 'success')
    
    return redirect(url_for('upload_page_view'))

@app.route('/messages')
def get_messages():
    return send_file('messages.json', mimetype='application/json')

@app.route('/submit_constraints', methods=['POST'])
def submit_constraints():
    # HTML formundan gelen verileri alın
    exam_start_date = request.form['examStartDate']
    exam_end_date = request.form['examEndDate']
    num_exams_per_day = int(request.form['numExamsPerDay'])
    friday_prayer_start_time = request.form['fridayPrayerStart']
    friday_prayer_end_time = request.form['fridayPrayerEnd']
    
    # exams için boş bir liste oluştur
    exams = []
    # numExamsPerDay değeri kadar sınav için döngü oluştur
    for i in range(1, num_exams_per_day + 1):
        exam_start_time = request.form[f'examStart{i}']
        exam_end_time = request.form[f'examEnd{i}']
        # Her sınav için startTime ve endTime alanlarını oluştur
        exam = {
            f"startTime{i}": exam_start_time,
            f"endTime{i}": exam_end_time
        }
        exams.append(exam)

    # Belirli bir JSON formatında Python sözlüğü oluşturun
    data = {
        "examDates": {
            "startDate": exam_start_date,
            "endDate": exam_end_date
        },
        "numExamsPerDay": num_exams_per_day,
        "exams": exams,
        "fridayPrayerTimes": {
            "startTime": friday_prayer_start_time,
            "endTime": friday_prayer_end_time
        }
    }

    # JSON formatındaki veriyi dosyaya yazma
    with open('uploaded_files/constraints.json', 'w') as json_file:
        json.dump(data, json_file)

    return jsonify({"message": "Form data received and processed successfully!"})


# Run the exam scheduler
@app.route('/run_exam_scheduler', methods=['POST'])
def run_exam_scheduler():
    full_path = app.config['OUTPUT_FOLDER']
    if os.path.exists(full_path):
        shutil.rmtree(full_path)
    os.makedirs(full_path)
    try:
        # Run the SyllabusScheduler.py script
        subprocess.run(["python", "SyllabusScheduler.py"], check=True)
        flash("SyllabusScheduler executed successfully.", "success")
    except subprocess.CalledProcessError:
        flash("SyllabusScheduler failed to execute.", "error")

    # Redirect to the schedule page
    return redirect(url_for('schedule_page_view'))


@app.route('/get_csv', methods=['GET'])
def get_csv():
    csv_path = os.path.join(OUTPUT_FOLDER, "exam_schedule.csv")  
    if os.path.exists(csv_path):
        return send_file(csv_path, mimetype='text/csv')  # CSV file is sent to the user
    else:
        flash("CSV file not found.", 'error')  # File not found
        return "CSV file not found", 404


# The main function
if __name__ == "__main__":
    app.run(debug=True)  # Debug mode is enabled
