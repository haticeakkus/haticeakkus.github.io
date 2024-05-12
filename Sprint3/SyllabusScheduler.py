import copy
from CourseDataReader import CourseDataReader
from ClassDataReader import ClassDataReader
import pandas as pd
import numpy as np
import random
import math
import csv

class SyllabusSchedular:
    
    def __init__(self, csv_file_classroom, csv_files_courses):
        """
        Initializes the SyllabusSchedular instance.

        Parameters:
        - csv_files_courses (list): List of CSV file paths for courses to be processed.
        - csv_file_classroom (str): The CSV file path for classroom data.
        """
        # Create instances of CourseDataReader and ClassDataReader
        self.course_data_reader = CourseDataReader(csv_files_courses)
        self.class_data_reader = ClassDataReader(csv_file_classroom)
        
        # Process classroom data
        self.classroom_data = self.class_data_reader.process_class_data(self.class_data_reader.data)

        # Initialize an empty schedule
        # syllabus_schedular.init_blocked_hours()

        #Print course and classroom data
        #print("\n\n*************** Data for Courses ***************\n")
        #self.print_course_data()
        #print("\n\n*************** Data for Classrooms ***************\n")
        #self.print_classroom_data()

    def print_classroom_data(self):
        """
        Prints the data in the CSV file.
        If data is available, prints the classroom information.
        If no data is available, prints a message indicating that data could not be read.
        """
        if not self.class_data_reader.data.empty:
            # Process classroom data and print
            for class_info in self.classroom_data:
                print(class_info)
        else:
            print("Classroom data could not be read.")

    def print_course_data(self):
        """
        Prints the processed data for each CSV file.
        If data is available, iterates through each dataset and prints the course information.
        If no data is available, prints a message indicating that data could not be read.
        """
        if self.course_data_reader.data:
            for data_set in self.course_data_reader.data:
                # Extract the prefix from the CSV file
                prefix = data_set['prefix']
                print(f"\nProcessing {prefix} courses:")
                
                # Print the data
                for course_info in data_set['data']:
                    print(course_info)
        else:
            print("Courses data could not be read.")
        
        return course_info

    def init_empty_schedule(self):
        """
        Initializes an empty schedule for the courses.

        Returns:
        - empty_schedule (dict): Dictionary containing an empty schedule for the courses.
        """
        # Initialize an empty schedule
        empty_schedule = {"Room":{"Monday":{"09.00":{"department":"", "course":"", "number of student":"", "class":"", "lecturer":"","end time":""}},
            "Tuesday":{"09.00":{"department":"", "course":"", "number of student":"", "class":"", "lecturer":"","end time":""}},
            "Wednesday":{"09.00":{"department":"", "course":"", "number of student":"", "class":"", "lecturer":"","end time":""}},
            "Thursday":{"09.00":{"department":"", "course":"", "number of student":"", "class":"", "lecturer":"","end time":""}},
            "Friday":{"09.00":{"department":"", "course":"", "number of student":"", "class":"", "lecturer":"","end time":""}},
            "Saturday":{"09.00":{"department":"", "course":"", "number of student":"", "class":"", "lecturer":"","end time":""}}
            }}
        
        
        # # Belirli bir başlangıç ve bitiş tarihi
        # start_date = datetime.date(2024, 5, 2)
        # end_date = datetime.date(2024, 5, 8)

        # # Tüm günlerin listesi
        # all_days = [(start_date + datetime.timedelta(days=i)).strftime("%A") for i in range((end_date - start_date).days + 1)]

        # # Boş program
        # empty_schedule = {"Room": {}}
        # for day in all_days:
        #     empty_schedule["Room"][day] = {
        #         "09.00": {"department": "", "course": "", "number of student": "", "class": "", "lecturer": "", "end time": ""}
        #         # Diğer saatler için aynı yapıyı kullanabilirsiniz
        #     }

        # print(empty_schedule)


        # Add the classroom numbers to the empty schedule 
        for class_info in self.classroom_data:
            classroom_number = class_info['Classroom Number']
            empty_schedule[classroom_number] = copy.deepcopy(empty_schedule["Room"])
        
        del empty_schedule["Room"]

        # Add time slots to the empty schedule
        for course in empty_schedule:
            for day in empty_schedule[course]:
                time = "09.00"
                while time != "18.00":
                    empty_schedule[course][day][time] = {"department":"", "course":"", "number of student":"", "class":"", "lecturer":"","end time":""}
                    time = pd.to_datetime(time, format="%H.%M") + pd.DateOffset(minutes=90)
                    time = time.strftime("%H.%M")

        return empty_schedule   
        
    def init_blocked_hours(self ):
        """
        Initializes the blocked hours

        Returns:
        - schedule (dict): Dictionary containing the schedule with blocked hours
        """

        schedule = self.init_empty_schedule()

        for room in schedule:
            for day in schedule[room]:
                for time in schedule[room][day]:
                    if day == "Friday" and time == "12.00":
                        schedule[room][day][time]["course"] = "BLOCKED for the Friday Prayer"
                        schedule[room][day][time]["department"] = "BLOCKED for the Friday Prayer"
                        schedule[room][day][time]["number of student"] = "BLOCKED for the Friday Prayer"
                        schedule[room][day][time]["class"] = "BLOCKED for the Friday Prayer"
                        schedule[room][day][time]["lecturer"] = "BLOCKED for the Friday Prayer"
                        schedule[room][day][time]["end time"] = "BLOCKED for the Friday Prayer"

                        # Exam duration
                        exam_duration = 90
                        # Add exam duration to time to get end time
                        end_time = pd.to_datetime(time, format="%H.%M") + pd.DateOffset(minutes=exam_duration)
                        # Assign the end time to the schedule
                        schedule[room][day][time]["end time"] =  end_time.strftime("%H.%M")

        return schedule

    def handle_blocked_hours(self, day, start_time, duration):
        """
        Handles the blocked hours input

        Parameters
        ----------
        day: str
            The day of the blocked hours
        start_time: str
            The start time of the blocked hours
        duration: str
            The duration of the blocked hours
        """

        # Check if the day is valid
        if day not in self.empty_schedule:
            print("Invalid day: ", day, "\nExiting the program...")
            exit(1)

        # Check if the hours is valid
        if start_time not in self.empty_schedule[day]:
            print("Invalid start time: ", start_time, "\nExiting the program...")
            exit(1)

        # Check if the duration is valid
        if not duration.isnumeric():
            print("Invalid duration: ", duration, "\nExiting the program...")
            exit(1)


    def get_all_lecturers(self):
        """
        Retrieves all unique lecturers from the course data.

        Returns:
        - lecturers (list): List of all unique lecturers.
        """
        lecturers = set()

        for data_set in self.course_data_reader.data:
            for course_info in data_set['data']:
                lecturers.add(course_info['Lecturer'])

        return lecturers
    
    def get_all_departments(self):
        """
        Retrieves all unique departments from the course data.

        Returns:
        - departments (set): Set of all unique departments.
        """
        departments = set()

        for data_set in self.course_data_reader.data:
            for course_info in data_set['data']:
                departments.add(course_info['Department'])

        return departments
        
    def get_all_courses_of_professor(self, lecturers):
        '''
        Returns a dictionary containing the courses of each professor

        Parameters
        ----------
        lecturers: list
            The list of all lecturers
        
        Returns
        -------
        lecturer_course_info: dict
            A dictionary containing the courses of each professor
        '''
                    
        lecturer_course_info = {}

        for lecturer in lecturers:
            lecturer_courses = []
            for course in self.course_data_reader.data:
                for course_info in course['data']:
                    if course_info['Lecturer'] == lecturer:
                        lecturer_courses.append(course_info['Course_Code'])
            lecturer_course_info[lecturer] = lecturer_courses

        return lecturer_course_info

    def get_all_capacity_of_classrooms(self):
        """
        Retrieves the capacity of all classrooms.
        
        Returns
        -------
        classrooms_capacity: dict
            The capacity of all classrooms
            
            big_classrooms_capacity: dict
            The capacity of all big classrooms
            
            small_classrooms_capacity: dict
            The capacity of all small classrooms
        """
        
        classrooms_capacity = {"Room": {"Capacity":""}}
        big_classrooms_capacity = {"Room": {"Capacity":""}}
        small_classrooms_capacity = {"Room": {"Capacity":""}}   
        for class_info in self.classroom_data:
            room = class_info['Classroom Number']
            classrooms_capacity[room] = class_info['Capacity']

            if class_info['Capacity'] >= 40:
                big_classrooms_capacity[room] = class_info['Capacity']
            else :
                small_classrooms_capacity[room] = class_info['Capacity']
        return classrooms_capacity,big_classrooms_capacity,small_classrooms_capacity
        
    def get_classroom_capacity(self, room):
        """
        Retrieves the capacity of a classroom.

        Parameters
        ----------
        room: str
            The room number

        Returns
        -------
        capacity: int
            The capacity of the classroom
        """
        for class_info in self.classroom_data:
            if class_info['Classroom Number'] == room:
                capacity = class_info['Capacity']
                return capacity 

    def professor_has_two_exams_at_same_time(self, professor_name, schedule):
        """
        Checks if a professor has two exams at the same time

        Parameters
        ----------
        professor_name: str
            The name of the professor
        schedule: dict
            The schedule

        Returns
        -------
        count: int
            The count of the exams at the same time
        conflict_lecturer_infos: list
            The list of conflict lecturer infos
        """

        count = 0
        info = []   
        conflict_lecturer_infos = []
        
        for room in schedule:
            for day in schedule[room]:
                for time in schedule[room][day]:
                    if schedule[room][day][time]["lecturer"] == professor_name:
                        info.append([professor_name,room, day, time, schedule[room][day][time]["course"], schedule[room][day][time]["number of student"], schedule[room][day][time]["class"], schedule[room][day][time]["end time"], schedule[room][day][time]["department"]])
        
        # find the exam at the same time in different room
        for i in range(len(info)):
            for j in range(i+1, len(info)):
                if info[i][2] == info[j][2] and info[i][3] == info[j][3] and info[i][4] != info[j][4]:
                    count+=1
                    conflict_lecturer_infos.append(info[i])
                    conflict_lecturer_infos.append(info[j])        

        return count, conflict_lecturer_infos
    
    def check_class_department_conflicts(self, schedule):
        conflict_class_infos = []
        conflict_capacity_cost = 0
        for room in schedule:
            for day in schedule[room]:
                for time in schedule[room][day]:
                    # Extract department and class from the scheduled exam
                    department = schedule[room][day][time]["department"]
                    course = schedule[room][day][time]["class"]
                    course_code = schedule[room][day][time]["course"]
                    lecturer = schedule[room][day][time]["lecturer"]
                    number_of_students = schedule[room][day][time]["number of student"]
                    
                    # Check if the department has already been scheduled in the same room at the same time
                    if department != "" and self.has_department_exam_conflict(schedule, room, day, time, department, course, course_code):
                        conflict_class_infos.append((room, day, time, course, course_code, department))
                        conflict_capacity_cost += 1
        
        return conflict_capacity_cost, conflict_class_infos
    
    def has_department_exam_conflict(self, schedule, room, day, time, department, course, course_code):
        """
        Checks if there's a departmental exam conflict for the given room, day, time, department, and course.

        Parameters
        ----------
        schedule: dict
            The schedule dictionary
        room: str
            The room where the exam is scheduled
        day: str
            The day of the exam
        time: str
            The time of the exam
        department: str
            The department of the exam
        course: str
            The course code of the exam

        Returns
        -------
        conflict: bool
            True if there's a departmental exam conflict, False otherwise
        """
        
        for other_room in schedule:
            if other_room != room:
                # Check if there's an exam scheduled for the same department in another room at the same time
                if schedule[other_room][day][time]["department"] == department and schedule[other_room][day][time]["class"] == course and schedule[other_room][day][time]["course"] != course_code:
                    return True
        
        return False
   
    def check_class_capacity_conflicts(self, schedule):
        """
        Checks for conflicts where classes have exams in rooms with insufficient capacity.

        Parameters
        ----------
        schedule: dict
            The schedule dictionary

        Returns
        -------
        count: int
            The count of the conflicts
        conflicts: list
            List of conflicts found
        """
        conflict_capacity_infos = []
        count = 0
        capacity = 0
        new_schedule = copy.deepcopy(schedule)
        department_course_capacity_info = {}

        for room in schedule:
            for day in schedule[room]:
                for time in schedule[room][day]:
                    number_of_students = schedule[room][day][time]["number of student"]
                    department = schedule[room][day][time]["department"]
                    class_number = schedule[room][day][time]["class"]
                    course_code = schedule[room][day][time]["course"]
                    lecturer = schedule[room][day][time]["lecturer"]
                    end_time = schedule[room][day][time]["end time"]
                    
                    if course_code != '' and course_code != "BLOCKED for the Friday Prayer": 
                        capacity = self.get_classroom_capacity(room)

                        if department not in department_course_capacity_info:
                            department_course_capacity_info[department] = {}

                        if course_code not in department_course_capacity_info[department]:
                            department_course_capacity_info[department][course_code] = {"number_of_students": number_of_students, "total_capacity": capacity}

                        min_capacity = ''
                        if capacity > number_of_students:
                            # print("Enough capacity for the exam.")
                            for room_s in new_schedule:
                                for day_s in new_schedule[room_s]:
                                    for time_s in new_schedule[room_s][day_s]:
                                        if new_schedule[room_s][day_s][time_s]["course"] == '' and day == day_s and time == time_s:
                                            room_capacity = self.get_classroom_capacity(room_s)
                                            # Find the class with the smallest empty capacity on the same day and time.
                                            if room_capacity < capacity and room_capacity >= number_of_students:
                                                min_capacity = room_capacity
                                                min_capacity_room = room_s
                                                for room_capacity_info in self.classroom_data:
                                                    if room_capacity_info['Classroom Number'] == room_s:
                                                        if room_capacity_info['Capacity'] < min_capacity:
                                                            min_capacity = room_capacity_info['Capacity']
                                                            min_capacity_room = room_s
                            # Place them in the smallest available classroom on the same day and time.
                            if min_capacity != '':
                                for room_m_c in new_schedule:
                                    for day_m_c in new_schedule[room_m_c]:
                                        for time_m_c in new_schedule[room_m_c][day_m_c]:
                                            if new_schedule[room_m_c][day_m_c][time_m_c]["course"] == '' and day == day_m_c and time == time_m_c and min_capacity_room == room_m_c:
                                                room_m_capacity = self.get_classroom_capacity(room_m_c)
                                                if  room_m_capacity == min_capacity:
                                                    # print(course_code, number_of_students, capacity, min_capacity)
                                                    new_schedule[room][day][time]["department"] = ''
                                                    new_schedule[room][day][time]["course"] = ''
                                                    new_schedule[room][day][time]["number of student"] = ''
                                                    new_schedule[room][day][time]["class"] = ''
                                                    new_schedule[room][day][time]["lecturer"] = ''
                                                    new_schedule[room][day][time]["end time"] = ''

                                                    new_schedule[room_m_c][day_m_c][time_m_c]["department"] = department
                                                    new_schedule[room_m_c][day_m_c][time_m_c]["course"] = course_code
                                                    new_schedule[room_m_c][day_m_c][time_m_c]["number of student"] = number_of_students
                                                    new_schedule[room_m_c][day_m_c][time_m_c]["class"] = class_number
                                                    new_schedule[room_m_c][day_m_c][time_m_c]["lecturer"] = lecturer
                                                    new_schedule[room_m_c][day_m_c][time_m_c]["end time"] = end_time
                                                    department_course_capacity_info[department][course_code]["total_capacity"] = room_m_capacity
                                                    break
         
                        else:
                            capacity = self.get_classroom_capacity(room)
                            remaining_students = number_of_students - capacity
                            for room_s in new_schedule:
                                for day_s in new_schedule[room_s]:
                                    for time_s in new_schedule[room_s][day_s]:
                                        if new_schedule[room_s][day_s][time_s]["course"] == '' and day == day_s and time == time_s:
                                            room_capacity = self.get_classroom_capacity(room_s)
                                            if remaining_students != 0:
                                                #  If the class added later is enough for the entire exam on its own, empty the first one.
                                                if room_capacity >= number_of_students:
                                                    # print(course_code, number_of_students, capacity, room_capacity)
                                                    new_schedule[room][day][time]["department"] = ''
                                                    new_schedule[room][day][time]["course"] = ''
                                                    new_schedule[room][day][time]["number of student"] = ''
                                                    new_schedule[room][day][time]["class"] = ''
                                                    new_schedule[room][day][time]["lecturer"] = ''
                                                    new_schedule[room][day][time]["end time"] = ''

                                                    new_schedule[room_s][day_s][time_s]["department"] = department 
                                                    new_schedule[room_s][day_s][time_s]["course"] = course_code
                                                    new_schedule[room_s][day_s][time_s]["number of student"] = number_of_students
                                                    new_schedule[room_s][day_s][time_s]["class"] = class_number
                                                    new_schedule[room_s][day_s][time_s]["lecturer"] = lecturer
                                                    new_schedule[room_s][day_s][time_s]["end time"] = end_time
                                                    remaining_students = 0
                                                    department_course_capacity_info[department][course_code]["total_capacity"] = room_capacity
                                                    break
                                            
                                                # if room_capacity >= remaining_students:
                                                #     new_schedule[room_s][day_s][time_s]["department"] = department
                                                #     new_schedule[room_s][day_s][time_s]["course"] = course_code
                                                #     new_schedule[room_s][day_s][time_s]["number of student"] = number_of_students
                                                #     new_schedule[room_s][day_s][time_s]["class"] = class_number
                                                #     new_schedule[room_s][day_s][time_s]["lecturer"] = lecturer
                                                #     new_schedule[room_s][day_s][time_s]["end time"] = end_time
                                                #     remaining_students = 0
                                                #     department_course_capacity_info[department][course_code]["total_capacity"] += room_capacity
                                                #     break  
                                                else:
                                                    new_schedule[room_s][day_s][time_s]["department"] = department
                                                    new_schedule[room_s][day_s][time_s]["course"] = course_code
                                                    new_schedule[room_s][day_s][time_s]["number of student"] = number_of_students
                                                    new_schedule[room_s][day_s][time_s]["class"] = class_number
                                                    new_schedule[room_s][day_s][time_s]["lecturer"] = lecturer
                                                    new_schedule[room_s][day_s][time_s]["end time"] = end_time
                                                    remaining_students -= room_capacity
                                                    department_course_capacity_info[department][course_code]["total_capacity"] += room_capacity
                                                    if remaining_students <= 0:
                                                        remaining_students = 0
                                                        break

        for department in department_course_capacity_info:
            for course_code in department_course_capacity_info[department]:
                # print("Department: ", department, "Course: ", course_code, "Total Capacity: ", department_course_capacity_info[department][course_code]["total_capacity"], "Number of Students: ", department_course_capacity_info[department][course_code]["number_of_students"])
                if department_course_capacity_info[department][course_code]["number_of_students"] > department_course_capacity_info[department][course_code]["total_capacity"]:
                    conflict_capacity_infos.append(course_code)
                    count += 1
                    print("Course has more students than the total capacity of the classrooms: ", course_code)

        return count, conflict_capacity_infos, new_schedule


    # def solve_conflict_capacity(self, schedule, conflict):


    #     room, day, time, end_time, course_code,  number_of_students, lecturer, department, course = conflict
    #     total_capacity = 0
    #     print("room: ", room, "day: ", day, "time: ", time, "end_time: ", end_time, "course_code: ", course_code, "number_of_students: ", number_of_students, "lecturer: ", lecturer, "department: ", department, "course: ", course)
    #     for class_info in self.classroom_data:
    #         if class_info['Classroom Number'] == room: 
    #             total_capacity = class_info['Capacity']
        
    #     for room_s in schedule:
    #         for day_s in schedule[room_s]:
    #             for times_s in schedule[room_s][day_s]:
    #                 while total_capacity < number_of_students and schedule[room_s][day_s][times_s]["course"] == "" :
    #                     if day_s == day and times_s == time:
    #                         for class_info in self.classroom_data:
    #                             if class_info['Classroom Number'] == room_s: 

    #                                 total_capacity += class_info['Capacity']
    #                                 schedule[room_s][day_s][times_s]["department"] = department
    #                                 schedule[room_s][day_s][times_s]["course"] = course_code
    #                                 schedule[room_s][day_s][times_s]["number of student"] = number_of_students
    #                                 schedule[room_s][day_s][times_s]["class"] = course
    #                                 schedule[room_s][day_s][times_s]["lecturer"] = lecturer
    #                                 schedule[room_s][day_s][times_s]["end time"] = end_time
    #                                 print("**********************************")
    #                                 print(room_s, day_s, times_s,  schedule[room_s][day_s][times_s]["department"], schedule[room_s][day_s][times_s]["course"], schedule[room_s][day_s][times_s]["number of student"], schedule[room_s][day_s][times_s]["class"], schedule[room_s][day_s][times_s]["lecturer"], room_s ,day_s,times_s, schedule[room_s][day_s][times_s]["end time"])
    #                                 print("**********************************")
    #                     else:
    #                         break   
    #     return

    def has_multiple_exams_on_day(self, schedule, department, class_number, day):
        """
        Checks if a department and class combination has more than one exam in a day for a given schedule.

        Parameters:
        schedule (dict): The schedule to check.
        department (str): The department to check.
        class_number (str): The class number to check.
        day (str): The day to check.

        Returns:
        bool: True if the department and class combination has two or more exams in the day, False otherwise.
        """
        # Count the number of exams for the department and class combination
        count = 0
        for room in schedule:
            for time in schedule[room][day]:
                if schedule[room][day][time]["department"] == 'BLOCKED for the Friday Prayer' or schedule[room][day][time]["class"] == 'BLOCKED for the Friday Prayer' or schedule[room][day][time]["course"] == 'BLOCKED for the Friday Prayer':
                    continue
                else:
                    if schedule[room][day][time]["department"] == department and schedule[room][day][time]["class"] == class_number and schedule[room][day][time]["course"] != "":
                        count += 1
                        if count > 2:
                            return True
        return False
    
    def check_multiple_exams_on_day_conflicts(self, schedule):
        """
        Checks for conflicts where a department-class combination
        has more than one exam in a day.
        
        Parameters
        ----------
        schedule: dict
            The schedule dictionary

        Returns
        -------
        conflict_multiple_exam_infos: list
            List of conflicts found
        """
        conflict_multiple_exam_infos = []
        control_conflict_multiple_exam_infos = []
        count = 0
        control = 0
        # Iterate over each department-class combination
        for room in schedule:
            for day in schedule[room]:
                for time in schedule[room][day]:
                    if schedule[room][day][time]["course"] != "":
                        department = schedule[room][day][time]["department"]
                        class_number = schedule[room][day][time]["class"]
                        end_time = schedule[room][day][time]["end time"]
                        course_code = schedule[room][day][time]["course"]
                        number_of_students = schedule[room][day][time]["number of student"]
                        lecturer = schedule[room][day][time]["lecturer"]
                        # Check if this combination has more than one exam in the day
                        if self.has_multiple_exams_on_day(schedule, department, class_number, day):
                            control += 1
                            if control > 2:
                                if room != '' and day != '' and time != '' and end_time != '' and department != '' and course_code != '' and class_number != '' and number_of_students != '' and lecturer != '':
                                    control_conflict_multiple_exam_infos.append((room, day, time, end_time, department, course_code, class_number, number_of_students, lecturer))
                                    if control_conflict_multiple_exam_infos != []:
                                        conflict_multiple_exam_infos = control_conflict_multiple_exam_infos
                                        count += 1
                                    
        return count, conflict_multiple_exam_infos

    def check_consecutive_exams_conflict(self, schedule):
        """
        Checks for conflicts where a department-class combination
        has exams on consecutive days.
        
        Parameters
        ----------
        schedule: dict
            The schedule dictionary

        Returns
        -------
        conflict_consecutive_exam_infos: list
            List of conflicts found
        """
        conflict_consecutive_exam_infos = []
        control_conflict_consecutive_exam_infos = []
        count = 0
        # Iterate over each department-class combination
        for room in schedule:
            for day in schedule[room]:
                for time in schedule[room][day]:
                    if schedule[room][day][time]["course"] != "":
                        department = schedule[room][day][time]["department"]
                        class_number = schedule[room][day][time]["class"]
                        course_code = schedule[room][day][time]["course"]
                        lecturer = schedule[room][day][time]["lecturer"]
                        number_of_students = schedule[room][day][time]["number of student"]
                        end_time = schedule[room][day][time]["end time"]
                        # Check if this combination has exams on consecutive days
                        if self.has_consecutive_exams(schedule, department, class_number, day, time, end_time):
                            control_conflict_consecutive_exam_infos.append((room, day, time, end_time, department, course_code, class_number, number_of_students, lecturer))
                            if control_conflict_consecutive_exam_infos != []:
                                for conflict in control_conflict_consecutive_exam_infos:
                                    if conflict_consecutive_exam_infos != []:
                                        flag = 0
                                        for conflict_asil in conflict_consecutive_exam_infos:
                                            if conflict == conflict_asil:
                                                flag = 1
                                                break
                                            
                                        if flag == 0:
                                            if conflict[5] != conflict_asil[5]:
                                                conflict_consecutive_exam_infos.append(conflict)
                                                count += 1
                                            
                                    else:
                                        conflict_consecutive_exam_infos.append(conflict)
                                        count += 1

        return count, conflict_consecutive_exam_infos

    def has_consecutive_exams(self, schedule, department, class_number, day, time, end_time):
        for other_room in schedule:
            for other_day in schedule[other_room]:
                for other_time in schedule[other_room][other_day]:
                    if schedule[other_room][other_day][other_time]["course"] != "":
                        if schedule[other_room][other_day][other_time]["department"] == department and schedule[other_room][other_day][other_time]["class"] == class_number and day == other_day and time == schedule[other_room][other_day][other_time]["end time"]:
                            # print("Consecutive Exam: ", department, class_number, day, time, end_time, other_time, schedule[other_room][other_day][other_time]["end time"])
                            return True

    def first_random_state(self, schedule):
        """
        The first random state for the schedule

        Parameters
        ----------
        schedule: dict
            The schedule

        Returns
        -------
        temp_schedule: dict
            The temporary schedule
        empty_times: list
            The list of empty times
        """
        temp_schedule = copy.deepcopy(schedule)

        # Get all empty times
        empty_times = []
        for room in temp_schedule:
            for day in temp_schedule[room]:
                for time in temp_schedule[room][day]:
                    if temp_schedule[room][day][time]["course"] == "":
                        empty_times.append((room, day, time))

        # Randomly assign courses to empty times
        for data_set in self.course_data_reader.data:
            #print("Data Set: ", data_set)   
            for course_info in data_set['data']:
                department = course_info["Department"]
                course = course_info["Course_Code"]
                number_of_students = course_info["Number_of_Students"]
                class_number = course_info["Class"]
                lecturer = course_info["Lecturer"]
                # Get random empty day and time to move course to
                idx = np.random.choice(len(empty_times))
                random_room, random_day, random_time = empty_times[idx]
                # Assign the course to the random empty time
                temp_schedule[random_room][random_day][random_time]["department"] = department
                temp_schedule[random_room][random_day][random_time]["course"] = course
                temp_schedule[random_room][random_day][random_time]["number of student"] = number_of_students
                temp_schedule[random_room][random_day][random_time]["class"] = class_number
                temp_schedule[random_room][random_day][random_time]["lecturer"] = lecturer
                # Exam duration
                exam_duration = 90
                # Add exam duration to time to get end time
                end_time = pd.to_datetime(random_time, format="%H.%M") + pd.DateOffset(minutes=exam_duration)
                # Assign the end time to the schedule
                temp_schedule[random_room][random_day][random_time]["end time"] =  end_time.strftime("%H.%M")
                # Remove the empty time from the list
                empty_times.pop(idx)

        return temp_schedule, empty_times
    
    def cost(self, schedule, lecturers):
        """
        The cost function for the schedule

        Parameters
        ----------
        schedule: dict
            The schedule
        lecturers: list
            The list of all lecturers

        Returns
        -------
        cost: int
            The cost of the schedule
        conflict_lecturer_infos: list
            The list of conflict lecturer infos
        conflict_class_infos: list
            The list of conflict class infos
        conflict_capacity_infos: list
            The list of conflict capacity infos
        conflict_multiple_exam_infos: list
            The list of conflict multiple exam infos
        conflict_consecutive_exams_infos: list
            The list of conflict consecutive exams infos
        """
        cost = 0
        conflict_lecturer_infos=[]
        conflict_lecturer_infos_control=[]
        conflict_class_cost, conflict_class_infos = self.check_class_department_conflicts(schedule) 
        conflict_multiple_exam_cost, conflict_multiple_exam_infos = self.check_multiple_exams_on_day_conflicts(schedule)
        conflict_consecutive_exams_cost, conflict_consecutive_exams_infos =  syllabus_schedular.check_consecutive_exams_conflict(schedule)


        #conflict_capacity_cost, conflict_capacity_infos, schedule_from_capacity = self.check_class_capacity_conflicts(schedule)

        for lecturer in lecturers:
            conflict_lecturer_cost, conflict_lecturer_info = self.professor_has_two_exams_at_same_time(lecturer, schedule)
            if(conflict_lecturer_info != []):
                for i in range(len(conflict_class_infos)):
                    if conflict_lecturer_info != conflict_class_infos[i]:
                        conflict_lecturer_infos_control = conflict_lecturer_info
                if conflict_lecturer_infos_control != []:     
                    cost += conflict_lecturer_cost   
                    conflict_lecturer_infos.append(conflict_lecturer_infos_control) 

        # print("*************** Conflict Lecturer ***************")
        # print(conflict_lecturer_infos)

        # print("*************** Conflict Class ***************")
        # print(conflict_class_infos)

        # # print("*************** Conflict Capacity ***************")
        # # print(conflict_capacity_infos)

        # print("*************** Conflict Multiple Exam ***************") 
        # print(conflict_multiple_exam_infos)


        cost += conflict_class_cost
        cost += conflict_multiple_exam_cost
        cost += conflict_consecutive_exams_cost
        #cost += conflict_capacity_cost

        return cost ,conflict_lecturer_infos, conflict_class_infos, conflict_multiple_exam_infos, conflict_consecutive_exams_infos
    
    def successor_move(self, old_schedule, cost, conflict_lecturer_infos, conflict_class_infos_t, conflict_multiple_exam_infos_t, conflict_consecutive_exams_infos_t, empty_times):
        """
        The successor move function for the schedule

        Parameters
        ----------
        old_schedule: dict
            The old schedule
        cost: int
            The cost of the schedule
        conflict_lecturer_infos: list
            The list of conflict lecturer infos
        conflict_class_infos: list
            The list of conflict class infos
        empty_times: list
            The list of empty times

        Returns
        -------
        new_schedule: dict
            The new schedule
        old_schedule: dict
            The old schedule
        """
        
        new_schedule = copy.deepcopy(old_schedule)
        
        lecturers = self.get_all_lecturers()
        empty_times = []
        for room in new_schedule:
            for day in new_schedule[room]:
                for time in new_schedule[room][day]:
                    if new_schedule[room][day][time]["course"] == "":
                        empty_times.append((room, day, time))

        #FIRST CONFLICT
        if(cost == 1):
            if (conflict_lecturer_infos != []):
                for room in new_schedule:
                    for day in new_schedule[room]:
                        for time in new_schedule[room][day]:
                            if new_schedule[room][day][time]["course"] == conflict_lecturer_infos[0][0][4]:
                                new_schedule[room][day][time]["department"] = ''
                                new_schedule[room][day][time]["course"] = ''
                                new_schedule[room][day][time]["number of student"] = ''
                                new_schedule[room][day][time]["class"] = ''
                                new_schedule[room][day][time]["lecturer"] = ''
                                new_schedule[room][day][time]["end time"] = ''

                                empty_times.append((room, day, time))

                idx = np.random.choice(len(empty_times))
                random_room, random_day, random_time = empty_times[idx]
                new_schedule[random_room][random_day][random_time]["department"] = conflict_lecturer_infos[0][0][8]
                new_schedule[random_room][random_day][random_time]["course"] = conflict_lecturer_infos[0][0][4]
                new_schedule[random_room][random_day][random_time]["number of student"] = conflict_lecturer_infos[0][0][5]
                new_schedule[random_room][random_day][random_time]["class"] = conflict_lecturer_infos[0][0][6]
                new_schedule[random_room][random_day][random_time]["lecturer"] = conflict_lecturer_infos[0][0][0]
                exam_duration = 90
                # Add exam duration to time to get end time
                end_time = pd.to_datetime(random_time, format="%H.%M") + pd.DateOffset(minutes=exam_duration)
                # Assign the end time to the schedule
                new_schedule[random_room][random_day][random_time]["end time"] =  end_time.strftime("%H.%M")
                # Remove the empty time from the list
                empty_times.pop(idx)

        else:
            if (conflict_lecturer_infos != []):
                
                first_conflict_lecturer_infos = []

                first_conflict_lecturer_infos.append(conflict_lecturer_infos[0][1][1])
                
                first_conflict_lecturer_infos.append(conflict_lecturer_infos[0][1][2])
                first_conflict_lecturer_infos.append(conflict_lecturer_infos[0][1][3])
                first_conflict_lecturer_infos.append(conflict_lecturer_infos[0][1][7])
      
                for i in range(len(conflict_lecturer_infos)-1):
                    
                    conflict_lecturer_infos[i][1][1] = conflict_lecturer_infos[i+1][1][1]
                    conflict_lecturer_infos[i][1][2] = conflict_lecturer_infos[i+1][1][2]
                    conflict_lecturer_infos[i][1][3] = conflict_lecturer_infos[i+1][1][3] 
                    conflict_lecturer_infos[i][1][7] = conflict_lecturer_infos[i+1][1][7]

                x = len(conflict_lecturer_infos)

                conflict_lecturer_infos[x-1][1][1] = first_conflict_lecturer_infos[0]
                conflict_lecturer_infos[x-1][1][2] = first_conflict_lecturer_infos[1]
                conflict_lecturer_infos[x-1][1][3] = first_conflict_lecturer_infos[2]
                conflict_lecturer_infos[x-1][1][7] = first_conflict_lecturer_infos[3]

        # update the new schedule
        if (conflict_lecturer_infos != []):
            for i in range(len(conflict_lecturer_infos)):
                for room in new_schedule:
                    for day in new_schedule[room]:
                        for time in new_schedule[room][day]:
                            if new_schedule[room][day][time]["course"] == conflict_lecturer_infos[i][1][4] and new_schedule[room][day][time]["department"] == conflict_lecturer_infos[i][1][8]:
                                new_schedule[room][day][time]["department"] = ''
                                new_schedule[room][day][time]["course"] = ''
                                new_schedule[room][day][time]["number of student"] = ''
                                new_schedule[room][day][time]["class"] = ''
                                new_schedule[room][day][time]["lecturer"] = ''
                                new_schedule[room][day][time]["end time"] = ''
                                break

            for i in range(len(conflict_lecturer_infos)):
                for room in new_schedule:
                    for day in new_schedule[room]:
                        for time in new_schedule[room][day]:
                            if room == conflict_lecturer_infos[i][1][1] and day == conflict_lecturer_infos[i][1][2] and time == conflict_lecturer_infos[i][1][3]:

                                new_schedule[room][day][time]["department"] = conflict_lecturer_infos[i][1][8]
                                new_schedule[room][day][time]["course"] = conflict_lecturer_infos[i][1][4]
                                new_schedule[room][day][time]["number of student"] = conflict_lecturer_infos[i][1][5]
                                new_schedule[room][day][time]["class"] = conflict_lecturer_infos[i][1][6]
                                new_schedule[room][day][time]["lecturer"] = conflict_lecturer_infos[i][1][0]
                                new_schedule[room][day][time]["end time"] = conflict_lecturer_infos[i][1][7]
                                break
                            
        old_cost, conflict_lecturer_infos_t, conflict_class_infos, conflict_multiple_exam_infos_t,conflict_consecutive_exams_infos_t = self.cost(new_schedule, lecturers)
        empty_times = []
        for room in new_schedule:
            for day in new_schedule[room]:
                for time in new_schedule[room][day]:
                    if new_schedule[room][day][time]["course"] == "":
                        empty_times.append((room, day, time))

        #SECOND CONFLICT
        if (conflict_class_infos != []):
            for conflict in conflict_class_infos:
                room, day, time, course, course_code, department = conflict
                # Find a suitable replacement slot for the conflicting exam
                idx = np.random.choice(len(empty_times))
                replacement_room, replacement_day, replacement_time  = empty_times[idx]
                #replacement_room, replacement_day, replacement_time = self.find_replacement_slot(new_schedule, room, day, time, course,course_code, department)
                #Perform the swap
                end_time = pd.to_datetime(replacement_time, format="%H.%M") + pd.DateOffset(minutes=90)   #Assuming exam duration is 90 minutes
                new_schedule[room][day][time], new_schedule[replacement_room][replacement_day][replacement_time] = new_schedule[replacement_room][replacement_day][replacement_time], new_schedule[room][day][time]
                new_schedule[replacement_room][replacement_day][replacement_time]["end time"] = end_time.strftime("%H.%M")  
                empty_times.pop(idx)


        old_cost, conflict_lecturer_infos_t, conflict_class_infos_t, conflict_multiple_exam_infos,conflict_consecutive_exams_infos_t = self.cost(new_schedule, lecturers)
    
        empty_times = []
        for room in new_schedule:
            for day in new_schedule[room]:
                for time in new_schedule[room][day]:
                    if new_schedule[room][day][time]["course"] == "":
                        empty_times.append((room, day, time))


        #THIRD CONFLICT

        if (conflict_multiple_exam_infos != []):
            for i in range(len(conflict_multiple_exam_infos)):
                for room in new_schedule:
                    for day in new_schedule[room]:
                        for time in new_schedule[room][day]:
                            if new_schedule[room][day][time]["course"] == conflict_multiple_exam_infos[i][5] and new_schedule[room][day][time]["department"] == conflict_multiple_exam_infos[i][4]:
                                new_schedule[room][day][time]["department"] = ''
                                new_schedule[room][day][time]["course"] = ''
                                new_schedule[room][day][time]["number of student"] = ''
                                new_schedule[room][day][time]["class"] = ''
                                new_schedule[room][day][time]["lecturer"] = ''
                                new_schedule[room][day][time]["end time"] = ''
                                empty_times.append((room, day, time))

                
                idx = np.random.choice(len(empty_times))
                random_room, random_day, random_time = empty_times[idx]

                while day == random_day:
                    idx = np.random.choice(len(empty_times))
                    random_room, random_day, random_time = empty_times[idx]


                idx = np.random.choice(len(empty_times))
                random_room, random_day, random_time = empty_times[idx]
                new_schedule[random_room][random_day][random_time]["department"] = conflict_multiple_exam_infos[i][4]
                new_schedule[random_room][random_day][random_time]["course"] = conflict_multiple_exam_infos[i][5]
                new_schedule[random_room][random_day][random_time]["number of student"] = conflict_multiple_exam_infos[i][7]
                new_schedule[random_room][random_day][random_time]["class"] = conflict_multiple_exam_infos[i][6]
                new_schedule[random_room][random_day][random_time]["lecturer"] = conflict_multiple_exam_infos[i][8]
                exam_duration = 90


                # Add exam duration to time to get end time
                end_time = pd.to_datetime(random_time, format="%H.%M") + pd.DateOffset(minutes=exam_duration)
                # Assign the end time to the schedule
                new_schedule[random_room][random_day][random_time]["end time"] =  end_time.strftime("%H.%M")
                # Remove the empty time from the list
                empty_times.pop(idx)

        old_cost, conflict_lecturer_infos_t, conflict_class_infos_t, conflict_multiple_exam_infos, conflict_consecutive_exams_infos = self.cost(new_schedule, lecturers)
        empty_times = []
        for room in new_schedule:
            for day in new_schedule[room]:
                for time in new_schedule[room][day]:
                    if new_schedule[room][day][time]["course"] == "":
                        empty_times.append((room, day, time))


        #FOURTH CONFLICT
        if (conflict_consecutive_exams_infos != []):
            for i in range(len(conflict_consecutive_exams_infos)):
                for room in new_schedule:
                    for day in new_schedule[room]:
                        for time in new_schedule[room][day]:
                            if new_schedule[room][day][time]["course"] == conflict_consecutive_exams_infos[i][5] and new_schedule[room][day][time]["department"] == conflict_consecutive_exams_infos[i][4]:
                                new_schedule[room][day][time]["department"] = ''
                                new_schedule[room][day][time]["course"] = ''
                                new_schedule[room][day][time]["number of student"] = ''
                                new_schedule[room][day][time]["class"] = ''
                                new_schedule[room][day][time]["lecturer"] = ''
                                new_schedule[room][day][time]["end time"] = ''
                                empty_times.append((room, day, time))

                
                idx = np.random.choice(len(empty_times))
                random_room, random_day, random_time = empty_times[idx]

                while day != random_day:
                    idx = np.random.choice(len(empty_times))
                    random_room, random_day, random_time = empty_times[idx]


                idx = np.random.choice(len(empty_times))
                random_room, random_day, random_time = empty_times[idx]
                new_schedule[random_room][random_day][random_time]["department"] = conflict_consecutive_exams_infos[i][4]
                new_schedule[random_room][random_day][random_time]["course"] = conflict_consecutive_exams_infos[i][5]
                new_schedule[random_room][random_day][random_time]["number of student"] = conflict_consecutive_exams_infos[i][7]
                new_schedule[random_room][random_day][random_time]["class"] = conflict_consecutive_exams_infos[i][6]
                new_schedule[random_room][random_day][random_time]["lecturer"] = conflict_consecutive_exams_infos[i][8]
                exam_duration = 90
                # Add exam duration to time to get end time
                end_time = pd.to_datetime(random_time, format="%H.%M") + pd.DateOffset(minutes=exam_duration)
                # Assign the end time to the schedule
                new_schedule[random_room][random_day][random_time]["end time"] =  end_time.strftime("%H.%M")
                # Remove the empty time from the list
                empty_times.pop(idx)

        return new_schedule, old_schedule
    
    
    
    def simulated_annealing_scheduler(self, temp_max, temp_min, cooling_rate, max_iter, K=1):
        """
        The simulated annealing scheduler
        
        Parameters
        ----------
        temp_max: float
            The maximum temperature
        temp_min: float
            The minimum temperature
        cooling_rate: float
            The cooling rate
        max_iter: int
            The maximum iteration
        K: int
            The K value

        Returns
        -------
        """

        print("\n\nStarting simulated annealing scheduler...\n")

        schedule , empty_times= self.first_random_state(self.init_blocked_hours())
        lecturers = self.get_all_lecturers()

        old_cost, conflict_lecturer_infos, conflict_class_infos, conflict_multiple_exam_infos, conflict_consecutive_exams_infos = self.cost(schedule, lecturers)
        iter_num = 0
        
        temperature = temp_max
        # While temperature is higher than minimum temperature
        while temperature >= temp_min:
            # While iteration number is lower than max iteration
            for i in range(max_iter):
                # Get the successor move
                schedule_after_update, schedule_before_update = self.successor_move(schedule, old_cost, conflict_lecturer_infos, conflict_class_infos, conflict_multiple_exam_infos, conflict_consecutive_exams_infos, empty_times)
                # Calculate the cost of the new schedule
                new_cost, conflict_lecturer_infos, conflict_class_infos, conflict_multiple_exam_infos, conflict_consecutive_exams_infos = self.cost(schedule_after_update, lecturers)
                print("Old Cost: ", old_cost)
                print("New Cost: ", new_cost)

                # If cost is 0 then return the schedule
                if new_cost == 0:
                    total = iter_num + i + 1
                    print(f"Found in {total}. iteration")
                    return schedule_after_update
                
                # Calculate delta
                delta = new_cost - old_cost
                if delta >= 0:
                    # If delta is positive then reject the move
                    if random.random() > math.exp(-1.0 * delta / (K * temperature)):
                        schedule = copy.deepcopy(schedule_before_update)
                    # Accept the bad move
                    else:
                        old_cost = new_cost
                        schedule = copy.deepcopy(schedule_after_update)
                # If delta is negative then accept the move
                else:
                    old_cost = new_cost
                    schedule = copy.deepcopy(schedule_after_update)
            # Update the iteration number and temperature
            iter_num += max_iter
            temperature *= cooling_rate

            # Print the iteration number and cost
            if iter_num % 50 == 0:
                print("Iteration: ", iter_num, "Fault Score: ", old_cost)


    def print_schedule(self, schedule):
        """
        Prints the schedule

        Parameters
        ----------
        schedule: dict
            The schedule
        """
        
        count = 0
        countClass = 0
        print("\n\n********************************************** SCHEDULE **********************************************\n")
        department_courses_class = {}

        for room in schedule:
            for day in schedule[room]:
                for time in schedule[room][day]:
                    course_info = schedule[room][day][time]
                    if course_info["course"] != "" and course_info["department"] != 'BLOCKED for the Friday Prayer' and course_info["course"] != 'BLOCKED for the Friday Prayer':
                        department = course_info["department"]
                        course = course_info["course"]
                        number_of_students = course_info["number of student"]
                        class_number = course_info["class"]
                        lecturer = course_info["lecturer"]
                        start_time = time
                        end_time = course_info["end time"]
                        room_w_capacity = f"{room} ({self.get_classroom_capacity(room)})"


                        course_details = (course, number_of_students, class_number , lecturer, room_w_capacity, day, start_time, end_time)
                        
                        if department not in department_courses_class:
                            department_courses_class[department] = {}

                        if class_number not in department_courses_class[department]:
                            department_courses_class[department][class_number] = [course_details]
                            
                        else:
                            # Check if the course already exists for this class
                            existing_courses = department_courses_class[department][class_number]
                            course_exists = False
                            for i, existing_course in enumerate(existing_courses):
                                if existing_course[0] == course:
                                    updated_course = list(existing_course)
                                    updated_course[4] += f" / {room} ({self.get_classroom_capacity(room)})"  # Append the room
                                    existing_courses[i] = tuple(updated_course)  # Update the tuple
                                    course_exists = True
                                    break
                            if not course_exists:
                                department_courses_class[department][class_number].append(course_details)
                
        exam = []
        # Print schedule
        for department, classes in department_courses_class.items():
            print(department)
            for class_number in sorted(classes.keys()):
                courses = classes[class_number]
                print(f"\tClass {class_number}:")
                countClass = 0
                for course_details in courses:
                    course, number_of_students, _, lecturer, room, day, start_time, end_time = course_details
                    if number_of_students == 0:
                        room = "ONLINE"
                        print(f"\t\t{course} ({number_of_students}) -> {lecturer}, {room}, {day}, {start_time} - {end_time}")
                        exam.append((department, class_number, course, number_of_students, lecturer, room, day, start_time, end_time))

                    else:
                        exam.append((department, class_number, course, number_of_students, lecturer, room, day, start_time, end_time))
                        print(f"\t\t{course} ({number_of_students}) -> {lecturer}, {room}, {day}, {start_time} - {end_time}")

                    count += 1
                    countClass += 1

        print(f"Total number of exams: {count}")
        return count,exam


if __name__ == "__main__":
    # Example: Create a SyllabusSchedular object using a sample CSV file
    csv_files_courses = [
        "uploaded_files/uploaded_course_files/CENG_Spring_Courses.csv",
        "uploaded_files/uploaded_course_files/CE_Spring_Courses.csv",
        "uploaded_files/uploaded_course_files/EE_Spring_Courses.csv",
        "uploaded_files/uploaded_course_files/ESE_Spring_Courses.csv",
        "uploaded_files/uploaded_course_files/IE_Spring_Courses.csv",
        "uploaded_files/uploaded_course_files/MATH_Spring_Courses.csv",
        "uploaded_files/uploaded_course_files/MCE_Spring_Courses.csv",
        "uploaded_files/uploaded_course_files/MSE_Spring_Courses.csv",
        "uploaded_files/uploaded_course_files/SENG_Spring_Courses.csv"
    ]
    csv_file_classroom = "uploaded_files/uploaded_classroom_files/Classrooms_and_Their_Capacities.csv"
    
    # Create a SyllabusSchedular object
    syllabus_schedular = SyllabusSchedular(csv_file_classroom, csv_files_courses)

    # Set the parameters for simulated annealing
    temp_max = 1.0 / 3
    temp_min = 0.0
    cooling_rate = 0.95
    max_iter = 10
    K = 1

    schedule = syllabus_schedular.simulated_annealing_scheduler(temp_max, temp_min, cooling_rate, max_iter, K)
    count, exam = syllabus_schedular.print_schedule(schedule)

    while count != 248:
        schedule = syllabus_schedular.simulated_annealing_scheduler(temp_max, temp_min, cooling_rate, max_iter, K)
        count, exam = syllabus_schedular.print_schedule(schedule)

    count_capacity, capacity_info, schedule = syllabus_schedular.check_class_capacity_conflicts(schedule)
    
    count, exam = syllabus_schedular.print_schedule(schedule)

    exam_schedule_csv_filename = "generated_files/exam_schedule.csv"
        # Open the CSV file in write mode
    with open(exam_schedule_csv_filename, mode='w', newline='', encoding='utf-8' ) as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Department", "Class", "Course Code", "Number of Students", "Lecturer", "Room", "Day", "Start Time", "End Time"])
        # Write the data rows 
        for department, class_number, course, number_of_students, lecturer, room, day, start_time, end_time in exam:
            writer.writerow([department, class_number, course, number_of_students, lecturer, room, day, start_time, end_time])

    print(f"Exam schedule times data has been written to {exam_schedule_csv_filename}")

    empty_times_csv_filename = "generated_files/empty_times.csv"

    empty_times = []
    for room in schedule:
        for day in schedule[room]:
            for time in schedule[room][day]:
                if schedule[room][day][time]["course"] == "":
                    empty_times.append((room, day, time))

    # Open the CSV file in write mode
    with open(empty_times_csv_filename, mode='w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["Room", "Day", "Time"])

        # Write the data rows
        for room, day, time in empty_times:
            writer.writerow([room, day, time])

    print(f"Empty times data has been written to {empty_times_csv_filename}")
