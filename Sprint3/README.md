# Exam Scheduler
Exam Scheduler is a web application designed to facilitate the creation of exam schedules for Ankara Yıldırım Beyazıt University. This tool allows administrators to upload course and classroom information, set constraints, and generate schedules efficiently.

## Features
- Upload Course Files: Administrators can upload CSV files containing course information for various departments.
- Upload Classroom Files: Classroom and capacity information can be uploaded using CSV files.
- Constraint Setting: Set constraints such as exam duration, start and end dates, and the number of exams per day.
- Dynamic Scheduler: The application dynamically generates schedules based on the uploaded data and constraints.
- View Schedule: Users can view the generated schedules through the web interface.
 
## Installation
To run this project locally, follow these steps:

Open the project directory and install the required dependencies:
```bash
pip install -r requirements.txt
```

Start the Flask application by running the following command:
```bash
flask run
```
Open your web browser and go to http://localhost:5000.
You will be directed to the application's home page. After performing the necessary actions, such as uploading files or setting constraints, you can perform operations such as creating a schedule or viewing a schedule.

## Usage
**1 -** Upon accessing the Landing Page, click on the designated button to proceed to the file upload page.

**2 -** On the file upload page, select the relevant CSV files containing course information from the spring_list folder. Ensure that the files are named appropriately and represent each department's courses accurately. After selecting the files, click on the "Upload Course Files" button to initiate the upload process.

**3 -** Under the "Classroom CSV" section, select the Classrooms_and_Their_Capacities" CSV file from the spring_list folder. This file should contain information about available classrooms and their capacities. Once selected, click on the "Upload Classroom CSV" button to complete the upload.

**4 -** Navigate to the constraint setting section and input the necessary constraints for scheduling. These may include specifying the exam duration, selecting the start and end dates of the exams, determining the number of exams to be held per day, and adding any additional constraints such as scheduling around Friday prayers.

**5 -** After setting the constraints, click on the "Run Scheduler" button to generate the exam schedule. The application will process the uploaded data and constraints to create an optimized schedule.

**6 -** Once the scheduler is created, you will be redirected to a new page where you can view the generated schedule. Click on the "Student Scheduler" button to access and review the schedule.


## Technologies
**jQuery UI Widget Datepicker**: This widget is used to select the start and end times of the exam in the area where constraints are entered on the Upload Files page.

**jQuery UI Dialog**: It serves as a warning when an incomplete file is uploaded on the Upload Files page, and provides informative content when a message is successfully sent on the Contact page.

**jQuery Validation**: This plugin is utilized to validate the form fields on the Contact Us page, ensuring that the user provides all necessary information before submitting the form. It displays error messages if any required fields are left empty or if an invalid email address is entered.

**jQuery UI Widget Spinner**: This widget is used to select how many exam days in the area where constraints are entered on the Upload Files page.

**jQuery UI Pluggin FadeIn FadeOut**: This pluggin is used to show Ankara Yıldırım Beyazıt University text in the main page.










