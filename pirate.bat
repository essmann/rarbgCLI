@echo off

:: Navigate to the folder containing your Python script
cd C:\CODING\Projects\Python\rarbg

:: Activate the virtual environment (change the path if needed)
call C:\CODING\Projects\Python\.venv\Scripts\activate.bat

:: Run the Python script with arguments passed to the batch file
python rarbg.py %*

:: Optionally deactivate the virtual environment after the script finishes
::deactivate