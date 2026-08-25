@echo off
REM Launches the K-OS Capture Hub. Keep this .bat next to kos_capture_hub.py.
REM Uses pythonw so no console window pops up. Change to `python` if you want to see stdout.
start "" pythonw.exe "%~dp0kos_capture_hub.py"
exit
