@echo off
echo Starting LLama Server...
echo.

REM Configuration
set MODEL_PATH=models\phi-4-mini-instruct-q4_k_m.gguf
set HOST=0.0.0.0
set PORT=8080
set CONTEXT_SIZE=4096
set THREADS=8
set GPU_LAYERS=0

REM Check if model exists
if not exist "%MODEL_PATH%" (
    echo Model file not found: %MODEL_PATH%
    echo Please place a GGUF model in the models\ directory
    pause
    exit /b 1
)

echo Configuration:
echo    Model: %MODEL_PATH%
echo    Host: %HOST%
echo    Port: %PORT%
echo    Context: %CONTEXT_SIZE%
echo    Threads: %THREADS%
echo.

echo Server will be available at: http://localhost:%PORT%
echo Press Ctrl+C to stop
echo.

server.exe ^
    -m "%MODEL_PATH%" ^
    --host "%HOST%" ^
    --port "%PORT%" ^
    -c "%CONTEXT_SIZE%" ^
    -t "%THREADS%" ^
    --n-gpu-layers "%GPU_LAYERS%"

echo.
echo Server stopped
pause
