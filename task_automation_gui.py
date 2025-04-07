import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from task_automation import TaskAutomation
import sys
from io import StringIO
import threading
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class TaskAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Automation Dashboard")
        self.root.geometry("1000x800")
        
        # Set theme
        self.style = ttk.Style(theme='darkly')
        
        # Create main container with padding
        self.main_container = ttk.Frame(root, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create content area
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create left and right panels
        self.left_panel = ttk.Frame(self.content_frame)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.right_panel = ttk.Frame(self.content_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Create input fields
        self.create_input_fields()
        
        # Create output area
        self.create_output_area()
        
        # Create status bar
        self.create_status_bar()
        
        # Redirect stdout to our output area
        self.stdout_redirect = StringIO()
        sys.stdout = self.stdout_redirect

    def create_header(self):
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="Task Automation Dashboard",
            font=("Helvetica", 24, "bold"),
            foreground="#ffffff"
        )
        title_label.pack(side=tk.LEFT)
        
        # Current time
        self.time_label = ttk.Label(
            header_frame,
            font=("Helvetica", 12),
            foreground="#ffffff"
        )
        self.time_label.pack(side=tk.RIGHT)
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def create_input_fields(self):
        # Input frame with modern styling
        input_frame = ttk.LabelFrame(
            self.left_panel,
            text="Task Parameters",
            padding="15"
        )
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas for scrolling
        canvas = tk.Canvas(input_frame)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Sheet URL
        self.create_input_row(scrollable_frame, "Google Sheet URL:", "sheet_url", 0)
        
        # Employee Email
        self.create_input_row(scrollable_frame, "Employee Email:", "emp_email", 1)
        
        # Employee Name
        self.create_input_row(scrollable_frame, "Employee Name:", "emp_name", 2)
        
        # Date
        self.create_input_row(scrollable_frame, "Date (YYYY-MM-DD):", "date", 3)
        
        # Task Count
        self.create_input_row(scrollable_frame, "Number of Tasks:", "task_count", 4)
        
        # Batch Number
        self.create_input_row(scrollable_frame, "Batch Number:", "batch_number", 5)
        
        # Time Parameters Frame
        time_frame = ttk.LabelFrame(scrollable_frame, text="Time Parameters", padding="10")
        time_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
        
        # T1
        self.create_input_row(time_frame, "T1 (max time):", "t1", 0, width=10)
        self.t1.insert(0, "16")
        
        # T2
        self.create_input_row(time_frame, "T2 (min time):", "t2", 1, width=10)
        self.t2.insert(0, "14")
        
        # T3
        self.create_input_row(time_frame, "T3 (avg time):", "t3", 2, width=10)
        self.t3.insert(0, "15.30")
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_input_row(self, parent, label_text, attr_name, row, width=50):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=5)
        entry = ttk.Entry(parent, width=width)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        setattr(self, attr_name, entry)

    def create_output_area(self):
        # Output frame with modern styling
        output_frame = ttk.LabelFrame(
            self.right_panel,
            text="Task Execution Log",
            padding="15"
        )
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Output text area with custom styling
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            width=50,
            height=20,
            font=("Consolas", 10),
            bg="#2b2b2b",
            fg="#ffffff"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(output_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Run button with icon
        self.run_button = ttk.Button(
            button_frame,
            text="▶ Run Automation",
            command=self.run_automation,
            style="success.TButton",
            width=20
        )
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button with icon
        self.clear_button = ttk.Button(
            button_frame,
            text="🗑 Clear Log",
            command=self.clear_output,
            style="danger.TButton",
            width=20
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def create_status_bar(self):
        self.status_bar = ttk.Label(
            self.main_container,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update_idletasks()

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.stdout_redirect = StringIO()
        sys.stdout = self.stdout_redirect
        self.update_status("Log cleared")

    def update_output(self):
        output = self.stdout_redirect.getvalue()
        if output:
            self.output_text.insert(tk.END, output)
            self.output_text.see(tk.END)
            self.stdout_redirect = StringIO()
            sys.stdout = self.stdout_redirect
        self.root.after(100, self.update_output)

    def run_automation(self):
        self.run_button.state(['disabled'])
        self.update_status("Running automation...")
        
        try:
            task_count = int(self.task_count.get())
        except ValueError:
            messagebox.showerror("Error", "Task count must be a number")
            self.run_button.state(['!disabled'])
            self.update_status("Error: Invalid task count")
            return
        
        automation = TaskAutomation()
        
        try:
            automation.T1 = float(self.t1.get())
            automation.T2 = float(self.t2.get())
            automation.T3 = float(self.t3.get())
        except ValueError:
            messagebox.showerror("Error", "Time parameters must be numbers")
            self.run_button.state(['!disabled'])
            self.update_status("Error: Invalid time parameters")
            return
        
        user_input = {
            'sheet_url': self.sheet_url.get(),
            'emp_email': self.emp_email.get(),
            'emp_name': self.emp_name.get(),
            'date': self.date.get(),
            'task_count': task_count,
            'batch_number': self.batch_number.get()
        }
        
        def run_thread():
            try:
                if not automation.authenticate('credentials.json'):
                    messagebox.showerror("Error", "Authentication failed")
                    self.update_status("Error: Authentication failed")
                    return
                
                if not automation.open_sheet(user_input['sheet_url']):
                    messagebox.showerror("Error", "Failed to open sheet")
                    self.update_status("Error: Failed to open sheet")
                    return
                
                row_range = automation.find_employee_row(
                    user_input['emp_email'],
                    user_input['date']
                )
                
                if not row_range:
                    messagebox.showerror("Error", "No matching rows found")
                    self.update_status("Error: No matching rows found")
                    return
                
                start_row, end_row = row_range
                
                if not automation.pre_fill_data(start_row, user_input):
                    messagebox.showerror("Error", "Failed to pre-fill data")
                    self.update_status("Error: Failed to pre-fill data")
                    return
                
                if automation.update_task_status(start_row, user_input['task_count']):
                    messagebox.showinfo("Success", "Tasks successfully updated!")
                    self.update_status("Tasks completed successfully")
                else:
                    messagebox.showerror("Error", "Failed to update tasks")
                    self.update_status("Error: Failed to update tasks")
            
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.update_status(f"Error: {str(e)}")
            
            finally:
                self.run_button.state(['!disabled'])
        
        threading.Thread(target=run_thread, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskAutomationGUI(root)
    app.update_output()
    root.mainloop() 