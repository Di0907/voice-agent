@echo off
setlocal ENABLEDELAYEDEXPANSION
title Voice Agent Launcher

REM --- Go to project root (this script's directory) ---
cd /d "%~dp0"

echo =====================================================
echo ===           Starting Voice Agent Demo...         ===
echo =====================================================
echo.

REM --- Sanity checks ---
if not exist "app.py" (
  echo [ERROR] app.py not found in %cd%
  echo Please run this script in the project root.
  pause
  goto :END
)

REM --- Pick Python (prefer venv) ---
set "PY_BIN="
set "USING_VENV="

if exist ".venv\Scripts\python.exe" (
  set "PY_BIN=.venv\Scripts\python.exe"
  set "USING_VENV=1"
) else (
  where python >nul 2>&1 && set "PY_BIN=python"
  if not defined PY_BIN (
    where py >nul 2>&1 && set "PY_BIN=py"
  )
)

if not defined PY_BIN (
  echo [ERROR] Python not found in PATH.
  echo Please install Python 3.10+ and/or create .venv first.
  pause
  goto :END
)

REM --- Define pip command bound to chosen Python ---
set "PIP_CMD=%PY_BIN% -m pip"

REM --- If using venv, try to activate for user comfort (optional) ---
if "%USING_VENV%"=="1" (
  if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
)

REM --- Check essential deps; install if missing ---
echo [INFO] Checking dependencies...
"%PY_BIN%" -c "import fastapi,uvicorn" >nul 2>&1
if errorlevel 1 (
  echo [INFO] Dependencies missing. Installing from requirements.txt...
  %PIP_CMD% install --upgrade pip
  %PIP_CMD% install -r requirements.txt
  if errorlevel 1 (
    echo.
    echo [ERROR] pip installation failed. Please check your network/permissions.
    pause
    goto :END
  )
  echo [INFO] Dependencies installed successfully.
)

REM --- Launch Backend (FastAPI + Uvicorn) ---
echo [INFO] Launching backend server...
start "Backend" cmd /k "%PY_BIN% -m uvicorn app:app --host 127.0.0.1 --port 8000"

REM --- Small wait so backend starts first ---
timeout /t 2 >nul

REM --- Launch Frontend (static files on 8080) ---
echo [INFO] Launching frontend server on port 8080...
start "Frontend - python -m http.server" cmd /k "%PY_BIN% -m http.server 8080"

REM --- Auto open browser to client page (best-effort) ---
set "TARGET_URL=http://127.0.0.1:8080/client/index.html"
echo [INFO] Opening %TARGET_URL%
start "" "%TARGET_URL%"

echo.
echo Voice Agent ready! If the browser didn't open, visit:
echo   %TARGET_URL%
echo.
pause

:END
endlocal
