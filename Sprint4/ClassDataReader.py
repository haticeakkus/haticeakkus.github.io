import pandas as pd

class ClassDataReader:
    def __init__(self, csv_file):
        """ Initializes the ClassDataReader instance
            Parameters is only Classrooms_and_Their_Capacities.csv
        """

        self.data = self.read_and_process_data(csv_file)

    
    def read_and_process_data(self, csv_file):
        """
        Reads and processes data from CSV file.
        Parameters:
        - csv_file : CSV file path for the csv file
        Returns:
        - data (list): List that containing data of csv file
        """

        classroom_data = []

        try:
            # Read the CSV file using pandas
            classroom_data = pd.read_csv(csv_file) 
        except FileNotFoundError:
            print(f"Error: {csv_file} not found.")
        
        return classroom_data
    

    def check_data_format(self, row):
        """
        Checks the format of a row in the CSV file.
        Parameters:
        - row (list): List representing a row of data in the CSV file.
        Raises:
        - ValueError: If the row does not have exactly 4 columns in the expected format.
        """
        expected_format = "Floor_Number,Classroom_Number,Capacity,Usage(How many days used for program)"
        if len(row) != 4:
            raise ValueError(f"Error: Each row must have exactly 4 columns. Expected format: {expected_format}")
        

    def process_class_data(self, data):
        """
        Processes classroom data from a pandas DataFrame.

        Parameters:
        - data (pd.DataFrame): DataFrame containing classroom data.

        Returns:
        - processed_data (list): List of dictionaries containing processed course information.
        """
        processed_data = []
        for row in data.values.tolist():
            try:
                # Check the format of the row
                self.check_data_format(row)
                # Extract relevant information from the row
                floor_Number = row[0]
                classroom_Number = row[1]
                capacity = row[2]
                usage = row[3]
                
                # Create a dictionary to store the processed information
                class_info = {
                    'Floor number': floor_Number,
                    'Classroom Number': classroom_Number,
                    'Capacity': capacity // 2,
                    'Usage': usage,
                    }
                
                # Append the dictionary to the list of processed data
                processed_data.append(class_info)
            except ValueError as e:
                print(f"Error in row: {row} - {e}")
        return processed_data



