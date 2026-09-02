@echo off
setlocal EnableExtensions

cd /d "%~dp0"

call :main >> backend_launcher.log 2>&1
exit /b %ERRORLEVEL%

:main
echo.
echo === Starting backend: %DATE% %TIME% ===

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  set "PYTHON_BIN=py -3"
) else (
  set "PYTHON_BIN=python"
)

if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -c "import sys; raise SystemExit(sys.version_info < (3, 10))"
  if ERRORLEVEL 1 (
    set "BACKUP=.venv.python-too-old.%RANDOM%"
    echo Existing .venv uses an unsupported Python version. Moving it to %BACKUP%
    ren ".venv" "%BACKUP%"
  )
)

if not exist ".venv\Scripts\activate.bat" (
  %PYTHON_BIN% -m venv .venv
)

call ".venv\Scripts\activate.bat"
echo Active venv Python:
python --version
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cd backend
python -m uvicorn main_API:app --host 127.0.0.1 --port 8000
