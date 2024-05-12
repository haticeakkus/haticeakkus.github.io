import pandas as pd

class CourseDataReader:
    def __init__(self, csv_files):
        """
        Initializes the CourseDataReader instance.

        Parameters:
        - csv_files (list): List of CSV file paths to be processed.
        """
        self.data = self.read_and_process_data(csv_files)

    def read_and_process_data(self, csv_files):
        """
        Reads and processes data from CSV files.

        Parameters:
        - csv_files (list): List of CSV file paths.

        Returns:
        - all_data (list): List of dictionaries containing processed data for each CSV file.
        """
        all_data = []
        for csv_file in csv_files:
            try:
                # Extract a specific prefix from the CSV file name
                prefix = csv_file.split('/')[1].split('_')[0]
                # Read the CSV file using pandas with UTF-8 encoding
                data = pd.read_csv(csv_file, encoding='utf-8')
                # Process the course data
                processed_data = self.process_course_data(data)
                # Append the processed data along with the prefix to the list
                all_data.append({'prefix': prefix, 'data': processed_data})
            except FileNotFoundError:
                print(f"Error: {csv_file} not found.")
        return all_data

    def check_data_format(self, row):
        """
        Checks the format of a row in the CSV file.

        Parameters:
        - row (list): List representing a row of data in the CSV file.

        Raises:
        - ValueError: If the row does not have exactly 10 columns in the expected format.
        """
        expected_format = "Section,Course_Code,Course_Name,Number_of_Students,Course_Environment,T+U,AKTS ,Class,Depertmant,Lecturer"
        if len(row) != 10:
            raise ValueError(f"Error: Each row must have exactly 10 columns. Expected format: {expected_format}")

    def process_course_data(self, data):
        """
        Processes course data from a pandas DataFrame.

        Parameters:
        - data (pd.DataFrame): DataFrame containing course data.

        Returns:
        - processed_data (list): List of dictionaries containing processed course information.
        """
        processed_data = []
        department_courses = {}  
        unique_entries = set()

        for row in data.values.tolist():
            try:
                # Check the format of the row
                self.check_data_format(row)
                # Extract relevant information from the row
                section = row[0]
                course_code = row[1]
                number_of_students = row[3]
                course_environment = row[4]
                t = row[5].split('+')[0]
                class_name = row[7]
                department = row[8]
                lecturer = row[9]
                
                # Check if the course environment contains "classroom"
                if "classroom" or "online" in course_environment.lower():
                    # Check if the course code has already been added for this department
                    if department not in department_courses:
                        department_courses[department] = set()
                    
                    if course_code not in department_courses[department]:
                        department_courses[department].add(course_code)
                        # Create a dictionary to store the processed information
                        if course_environment == "online":
                            number_of_students = 0

                        entry = (section, course_code, number_of_students, course_environment, t, class_name, lecturer)
                        
                        if entry not in unique_entries:
                            unique_entries.add(entry)
                            course_info = {
                                'Section': section,
                                'Course_Code': course_code,
                                'Number_of_Students': number_of_students,
                                'Course_Environment': course_environment,
                                'T+U(t)': t,
                                'Class': class_name,
                                'Department': department,
                                'Lecturer': lecturer
                            }
                            # Append the dictionary to the list of processed data
                            processed_data.append(course_info)
            except ValueError as e:
                print(f"Error in row: {row} - {e}")
        return processed_data

