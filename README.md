# 🚀 Task Automation Dashboard

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/GUI-Tkinter-green" alt="GUI Framework">
  <img src="https://img.shields.io/badge/Theme-Darkly-dark" alt="Theme">
</div>

## 📊 Overview

A modern, user-friendly dashboard for automating task management in Google Sheets. This application provides a sleek interface for tracking employee tasks, managing time parameters, and ensuring consistent task completion times.

## ✨ Features

- **Modern Dark Theme UI** - Sleek, professional interface with dark mode
- **Real-time Status Updates** - Live feedback on task execution
- **Time Parameter Controls** - Fine-tune task timing with T1, T2, and T3 parameters
- **Scrollable Input Area** - Handle large amounts of data with ease
- **Live Clock** - Current time display in the header
- **Task Execution Log** - Detailed output of automation progress
- **Error Handling** - Comprehensive error messages and status updates

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/itsmeayan45/task-automation.git
   cd task-automation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets API**
   - Create a project in [Google Cloud Console](https://console.cloud.google.com)
   - Enable the Google Sheets API
   - Create a service account and download credentials
   - Save the credentials file as `credentials.json` in the project directory

## 🖥️ Usage

1. **Launch the application**
   ```bash
   python task_automation_gui.py
   ```

2. **Enter task parameters**
   - Google Sheet URL
   - Employee Email
   - Employee Name
   - Date (YYYY-MM-DD)
   - Number of Tasks
   - Batch Number
   - Time Parameters (optional)

3. **Run the automation**
   - Click the "▶ Run Automation" button
   - Monitor progress in the Task Execution Log
   - Check the status bar for current operation status

## ⚙️ Configuration

### Time Parameters

- **T1**: Maximum task time (default: 16 minutes)
- **T2**: Minimum task time (default: 14 minutes)
- **T3**: Target average time (default: 15.30 minutes)

### Google Sheet Structure

The application expects a Google Sheet with the following columns:
- DATE
- FP EMP NAME
- TASK ID
- TASK ASSIGNED TO ME
- BATCH #
- FP EMP EMAIL
- Status
- Time Taken

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication Error | Check your credentials.json file |
| Sheet Access Error | Verify the Google Sheet URL and permissions |
| Invalid Input | Ensure all fields contain valid data |
| Task Update Failure | Check internet connection and sheet permissions |

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Your Name - Initial work

---

<div align="center">
  <p>Made with ❤️ for efficient task management</p>
</div> 
