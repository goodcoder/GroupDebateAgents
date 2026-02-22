@echo off
echo Stopping Streamlit App...
taskkill /F /IM streamlit.exe /T 2>nul
if %ERRORLEVEL% equ 0 (
    echo Successfully stopped Streamlit.
) else (
    echo Streamlit is not currently running.
)
