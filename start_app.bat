@echo off
echo Starting Group Debate Agents Streamlit App in the background...
call .\venv\Scripts\activate.bat
start "Streamlit App" /MIN streamlit run app.py
echo App is starting. You can close this terminal.
