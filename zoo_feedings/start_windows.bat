@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
.venv\Scripts\python.exe init_db.py
.venv\Scripts\python.exe manage.py check
if errorlevel 1 goto failed
.venv\Scripts\python.exe manage.py runserver --insecure
pause
exit /b
:failed
pause
exit /b 1
