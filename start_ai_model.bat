@echo off

cd ..

echo Starting SSC Thumbnail AI...
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build
if %errorlevel% neq 0 (
    echo Python script failed. Exiting.
    pause
    exit /b %errorlevel%
)
