import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import time
from datetime import datetime
import pandas as pd
from dateutil import parser

class TaskAutomation:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
        self.credentials = None
        self.client = None
        self.sheet = None
        self.T1 = 16  # Default Task 1 Time
        self.T2 = 14  # Default Task 2 Time
        self.T3 = 15.30  # Default Average Time
        self.headers = [
            'DATE', 'FP EMP NAME', 'TASK ID', 'TASK ASSIGNED TO ME',
            'BATCH #', 'FP EMP EMAIL', 'Status', 'Time Taken'
        ]

    def authenticate(self, credentials_file):
        """Authenticate with Google Sheets API"""
        try:
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                credentials_file, self.scope)
            self.client = gspread.authorize(self.credentials)
            return True
        except Exception as e:
            print(f"Authentication Error: {str(e)}")
            return False

    def open_sheet(self, sheet_url):
        """Open the Google Sheet using the provided URL"""
        try:
            self.sheet = self.client.open_by_url(sheet_url).sheet1
            return True
        except Exception as e:
            print(f"Error opening sheet: {str(e)}")
            return False

    def get_user_input(self):
        """Collect user input for task automation"""
        print("\n=== Task Automation Input ===")
        sheet_url = input("Enter Google Sheet URL: ")
        emp_email = input("Enter Employee Email: ")
        emp_name = input("Enter Employee Name: ")
        date_str = input("Enter Date (YYYY-MM-DD): ")
        task_count = int(input("Enter Number of Tasks: "))
        batch_number = input("Enter Batch Number: ")
        
        # Optional time parameters
        try:
            self.T1 = float(input(f"Enter T1 (default {self.T1}): ") or self.T1)
            self.T2 = float(input(f"Enter T2 (default {self.T2}): ") or self.T2)
            self.T3 = float(input(f"Enter T3 (default {self.T3}): ") or self.T3)
        except ValueError:
            print("Using default time values...")

        return {
            'sheet_url': sheet_url,
            'emp_email': emp_email,
            'emp_name': emp_name,
            'date': date_str,
            'task_count': task_count,
            'batch_number': batch_number
        }

    def find_employee_row(self, emp_email, date):
        """Find the row range for the specified employee and date"""
        try:
            # Get all values from the sheet
            all_values = self.sheet.get_all_values()
            
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(all_values[1:], columns=all_values[0])
            
            # Find rows matching the employee email and date
            matching_rows = df[
                (df['FP EMP EMAIL'] == emp_email) & 
                (df['DATE'] == date)
            ]
            
            if len(matching_rows) == 0:
                return None
            
            # Get the row numbers (add 2 to account for header row and 0-based index)
            row_numbers = [idx + 2 for idx in matching_rows.index]
            return min(row_numbers), max(row_numbers)
        except Exception as e:
            print(f"Error finding employee row: {str(e)}")
            return None

    def pre_fill_data(self, start_row, user_input):
        """Pre-fill the sheet with basic data"""
        try:
            for i in range(user_input['task_count']):
                current_row = start_row + i
                
                # Update basic information
                self.sheet.update_cell(current_row, 1, user_input['date'])  # DATE
                self.sheet.update_cell(current_row, 2, user_input['emp_name'])  # FP EMP NAME
                self.sheet.update_cell(current_row, 4, "Yes")  # TASK ASSIGNED TO ME
                self.sheet.update_cell(current_row, 5, user_input['batch_number'])  # BATCH #
                self.sheet.update_cell(current_row, 6, user_input['emp_email'])  # FP EMP EMAIL
                self.sheet.update_cell(current_row, 7, "In Progress")  # Status
                
                # Get task ID from user
                task_id = input(f"Enter Task ID for task {i+1}: ")
                self.sheet.update_cell(current_row, 3, task_id)  # TASK ID
                
            return True
        except Exception as e:
            print(f"Error pre-filling data: {str(e)}")
            return False

    def simulate_task_time(self):
        """Simulate task completion time between T1 and T2"""
        return random.uniform(self.T2, self.T1)

    def update_task_status(self, start_row, task_count):
        """Update task status and timing in the sheet"""
        try:
            total_time = 0
            times = []
            
            # First pass: simulate all times
            for _ in range(task_count):
                task_time = self.simulate_task_time()
                times.append(task_time)
                total_time += task_time
            
            # Adjust times if average is too far from T3
            avg_time = total_time / task_count
            if abs(avg_time - self.T3) > 0.5:  # If difference is more than 30 seconds
                adjustment_factor = self.T3 / avg_time
                times = [t * adjustment_factor for t in times]
            
            # Second pass: update sheet with adjusted times
            for i, task_time in enumerate(times):
                current_row = start_row + i
                
                # Update status to "Done"
                self.sheet.update_cell(current_row, 7, "Done")  # Status column
                
                # Update time taken
                self.sheet.update_cell(current_row, 8, f"{task_time:.2f}")  # Time Taken column
                
                # Simulate processing time
                time.sleep(1)
                
            return True
        except Exception as e:
            print(f"Error updating task status: {str(e)}")
            return False

    def run(self):
        """Main execution method"""
        # Get user input
        user_input = self.get_user_input()
        
        # Authenticate and open sheet
        if not self.authenticate('credentials.json'):
            return
        
        if not self.open_sheet(user_input['sheet_url']):
            return
        
        # Find employee row range
        row_range = self.find_employee_row(
            user_input['emp_email'], 
            user_input['date']
        )
        
        if not row_range:
            print("No matching rows found for the given employee and date.")
            return
        
        start_row, end_row = row_range
        
        # Pre-fill data
        if not self.pre_fill_data(start_row, user_input):
            print("Error pre-filling data. Aborting...")
            return
        
        # Update task status and timing
        if self.update_task_status(start_row, user_input['task_count']):
            print("\n✅ Tasks successfully updated!")
        else:
            print("\n❌ Error updating tasks.")

if __name__ == "__main__":
    automation = TaskAutomation()
    automation.run() 