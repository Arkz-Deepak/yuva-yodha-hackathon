@echo off
echo ========================================================
echo  EcoCast AI - Induction Furnace Digital Twin Gateway
echo  Schneider Electric Yuva Yodha Hackathon 2026
echo ========================================================
echo.
echo Starting backend server on http://localhost:8000 ...
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
pause
