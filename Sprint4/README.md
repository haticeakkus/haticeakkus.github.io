# Exam Scheduler
The exam scheduler project we developed for our university completely automates the process of creating the exam schedule, minimizing the errors and time loss associated with manual operations. Our product utilizes simulated annealing algorithms to optimize the exam schedule according to specified constraints and priorities. In doing so, we address challenges such as balancing classroom capacities, resolving conflicting exam schedules for students, ensuring a maximum of two exams per day according to designated exam durations, and accommodating special needs and even religious considerations to create the most suitable exam timetable. Moreover, we offer a user-friendly interface to ensure ease of use for everyone.

<br/>
Additionally, a video demonstration of the project has been included at the end of this document for your convenience.


## Features

- **Automatic Exam Schedule Generation:** Our project automates the cumbersome and time-consuming manual tasks involved in creating exam schedules, enabling users to swiftly generate schedules.

- **Flexible Constraint Management:** Users can define specific constraints during the exam schedule creation process, such as exam durations, exam days, and special requirements. Our project intelligently handles these constraints to produce optimal and well-balanced exam schedules.

- **Easy File Upload and Data Transfer:** Users can effortlessly upload CSV files to quickly transfer course and class information. Our project efficiently processes the uploaded data to generate the exam schedule.

- **Interactive and User-Friendly Interface:** With a user-friendly interface powered by jQuery UI components and custom plugins, our project offers users a guided, step-by-step experience to create exam schedules.

- **Error Handling and Real-Time Feedback:** Our project ensures minimal user errors through form validation and instant error messages. Users receive immediate feedback on any missing or incorrect information during data entry.

- **Progress Indicator and Real-Time Monitoring:** A progress bar visually tracks the exam schedule generation process, allowing users to monitor the progress of the operation in real-time.


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
You will be directed to the application's home page.

## Usage
- Upon accessing the Landing Page, click on the designated button to proceed to the file upload page.

- On the file upload page, select the relevant CSV files containing course information from the spring_list folder. Ensure that the files are named appropriately and represent each department's courses accurately. After selecting the files, click on the "Upload Course Files" button to initiate the upload process.

- Under the "Classroom CSV" section, select the Classrooms_and_Their_Capacities" CSV file from the spring_list folder. This file should contain information about available classrooms and their capacities. Once selected, click on the "Upload Classroom CSV" button to complete the upload.

- Navigate to the constraint setting section and input the necessary constraints for scheduling. These may include specifying the exam duration, selecting the start and end dates of the exams, determining the number of exams to be held per day, and adding any additional constraints such as scheduling around Friday prayers.

- After setting the constraints, click on the "Run Exam Scheduler" button to generate the exam schedule. The application will process the uploaded data and constraints to create an optimized schedule.

- Once the scheduler is created, you will be redirected to a new page where you can view the generated schedule. Click on the "Student Exam Schedule" button to access and review the schedule.


## Technologies used by GUI
Our website meets the assignment specifications through the implementation of various interactive functionalities:
- AJAX:
    -	On the Home Page, it fetches date and time values from the World Time API to display world clocks. ( https://worldtimeapi.org/ )
    -	The Home Page features texts that change every 2 seconds, updated with texts fetched from an external JSON file.
    -	On the Upload Page, it sends form data to the server and processes the response.

-	jQuery UI Widget:
    - Dialog: Warns users on the Upload Page if "Course" and "Classroom" files are not selected before submission. On the Contact Page, it displays a message confirming successful submission after relevant fields are filled.
    - Datepicker: Enables users to select dates for constraints on the Upload Page.

-	jQuery Plugin:
    - FadeIn FadeOut Plugin: Utilized to display "Ankara Yıldırım Beyazıt University" text on the main page.
    - Handler Plugin: Used to display information about selected files in the "Course" and "Classroom" sections of the Upload Page and append or update this information in the respective container.
    -	Progress Plugin: Displays a progress bar while the code for scheduling exams runs when the "Run Exam Scheduler" button is clicked. It shows the progress of the code execution and fills the bar at intervals.
    -	Validation Plugin: Validates form fields on the Contact Us page, ensuring all necessary information is provided before submission. It prompts error messages if required fields are left empty or if an invalid email address is entered.
 
## Video
[Click here for a video demonstration of the application in action.]( https://www.youtube.com/watch?v=_215wJRCmK8)