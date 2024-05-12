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


# Flask route to handle writing JSON data to file
@app.route('/write_constraints_json_to_file', methods=['POST'])
def write_json_to_file():
    data = request.get_json()

    # Write JSON data to a file
    file_path = 'json_constraints_data.json'  # File path
    with open(file_path, 'w') as file:
        json.dump(data, file)

    # Do any further processing with the JSON data if needed
    print('JSON data written to file:', file_path)

    return jsonify({'message': 'JSON data written to file'})



@app.route('/run_exam_scheduler', methods=['POST'])
def run_exam_scheduler():
    full_path = app.config['OUTPUT_FOLDER']
    if os.path.exists(full_path):
        shutil.rmtree(full_path)
    os.makedirs(full_path)
    try:
        # Run the SyllabusScheduler.py script
        subprocess.run(["python", "SyllabusScheduler.py"], check=True)
        flash("SyllabusScheduler çalıştırıldı.", "success")
    except subprocess.CalledProcessError:
        flash("SyllabusScheduler çalıştırılamadı.", "error")

    # Redirect to the schedule page
    return redirect(url_for('schedule_page_view'))



@app.route('/get_csv', methods=['GET'])
def get_csv():
    csv_path = os.path.join(OUTPUT_FOLDER, "exam_schedule.csv")  
    if os.path.exists(csv_path):
        return send_file(csv_path, mimetype='text/csv')  # CSV file is sent to the user
    else:
        flash("CSV dosyası bulunamadı.", 'error')  # File not found
        return "CSV dosyası bulunamadı", 404

# The main function
if __name__ == "__main__":
    app.run(debug=True)  # Debug mode is enabled
