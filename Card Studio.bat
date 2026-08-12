@echo off
setlocal
cd /d "%~dp0"
title Known Associates - Card Studio

echo.
echo   ==========================================
echo     KNOWN ASSOCIATES - CARD STUDIO
echo   ==========================================
echo.

REM --- find Python -----------------------------------------------------------
set "PY="
where py >nul 2>&1 && set "PY=py"
if not defined PY ( where python >nul 2>&1 && set "PY=python" )
if not defined PY (
  echo   Python is not installed, or Windows cannot find it.
  echo.
  echo   Install it from  https://www.python.org/downloads/
  echo   During setup, TICK THE BOX that says "Add python.exe to PATH".
  echo   Then run this file again.
  echo.
  pause
  exit /b 1
)

REM --- first run: build the private environment -------------------------------
if not exist ".venv\Scripts\python.exe" (
  echo   First run - setting up. This takes about a minute.
  echo.
  %PY% -m venv .venv
  if errorlevel 1 goto fail
)

".venv\Scripts\python.exe" -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto fail

REM --- go ---------------------------------------------------------------------
echo   Starting. Your browser will open in a few seconds.
echo.
echo   Leave this black window open while you work.
echo   Close it (or press Ctrl+C) when you're done.
echo.
".venv\Scripts\python.exe" tools\studio.py
goto end

:fail
echo.
echo   ------------------------------------------
echo   Setup failed. Copy everything above this
echo   line and send it to Claude.
echo   ------------------------------------------
echo.
pause
exit /b 1

:end
echo.
echo   Card Studio stopped.
timeout /t 3 >nul
