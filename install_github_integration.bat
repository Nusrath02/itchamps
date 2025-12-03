@echo off
REM Installation script for GitHub API integration (Windows)

echo ================================================
echo GitHub API Integration Installer (Windows)
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "env\Scripts\activate.bat" (
    echo [ERROR] Not in a Frappe bench directory
    echo Please run this script from your frappe-bench directory
    pause
    exit /b 1
)

echo Step 1: Installing Python dependencies...
call env\Scripts\activate.bat
pip install requests
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

echo Step 2: Clearing Frappe cache...
bench clear-cache
if %errorlevel% neq 0 (
    echo [WARNING] Cache clear failed (not critical)
) else (
    echo [OK] Cache cleared
)
echo.

echo Step 3: Building assets...
bench build
if %errorlevel% neq 0 (
    echo [WARNING] Build failed (not critical)
) else (
    echo [OK] Assets built
)
echo.

echo Step 4: Restarting Frappe...
bench restart
if %errorlevel% neq 0 (
    echo [ERROR] Failed to restart Frappe
    pause
    exit /b 1
)
echo [OK] Frappe restarted
echo.

echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Open your Frappe site in a browser
echo 2. Click the chatbot icon (robot emoji) in the navbar
echo 3. Try these commands:
echo    - "Show repo info"
echo    - "Show recent commits"
echo    - "Show open issues"
echo.
echo Optional: Add GitHub token for higher rate limits
echo See README_GITHUB_SETUP.md for instructions
echo.
echo Test the integration:
echo   cd apps\itchamps
echo   python test_github_integration.py
echo.
pause
