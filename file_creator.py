"""
File Creation Module
Creates startup scripts, test scripts, and directories
"""
import os


def create_startup_script(requirements):
    print("Creating startup script...")

    script_name = requirements["startup_script"]
    
    if requirements.get("system", "unknown") == "windows":
        script_content = '''@echo off
echo Starting LLama Server...
echo.

REM Configuration
set MODEL_PATH=models\\phi-4-mini-instruct-q4_k_m.gguf
set HOST=0.0.0.0
set PORT=8080
set CONTEXT_SIZE=4096
set THREADS=8
set GPU_LAYERS=0

REM Check if model exists
if not exist "%MODEL_PATH%" (
    echo Model file not found: %MODEL_PATH%
    echo Please place a GGUF model in the models\\ directory
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
'''
    else:
        script_content = '''#!/bin/bash
echo "Starting LLama Server..."
echo

# Configuration
MODEL_PATH="models/phi-4-mini-instruct-q4_k_m.gguf"
HOST="0.0.0.0"
PORT="8080"
CONTEXT_SIZE="4096"
THREADS="8"
GPU_LAYERS="0"

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "Model file not found: $MODEL_PATH"
    echo "Please place a GGUF model in the models/ directory"
    exit 1
fi

echo "Configuration:"
echo "   Model: $MODEL_PATH"
echo "   Host: $HOST"
echo "   Port: $PORT"
echo "   Context: $CONTEXT_SIZE"
echo "   Threads: $THREADS"
echo

echo "Server will be available at: http://localhost:$PORT"
echo "Press Ctrl+C to stop"
echo

./server \\
    -m "$MODEL_PATH" \\
    --host "$HOST" \\
    --port "$PORT" \\
    -c "$CONTEXT_SIZE" \\
    -t "$THREADS" \\
    --n-gpu-layers "$GPU_LAYERS"

echo
echo "Server stopped"
'''
    
    with open(script_name, 'w', newline='\n') as f:
        f.write(script_content)
    
    if requirements["needs_chmod"]:
        os.chmod(script_name, 0o755)
    
    print(f"Created {script_name}")


def create_test_script():
    print("Creating test script...")
    
    test_content = '''#!/usr/bin/env python3
"""
LLama Server API Test Script
"""
import requests
import json
import time

def test_server(base_url="http://localhost:8080"):
    print("Testing LLama Server API")
    print("=" * 40)

    print("1. Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   Server is healthy")
        else:
            print(f"   Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   Connection failed: {e}")
        return False

    print("\\n2. Models Endpoint...")
    try:
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"   Found {len(models.get('data', []))} model(s)")
        else:
            print(f"   Models endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   Models test failed: {e}")

    print("\\n3. Text Completion...")
    try:
        payload = {
            "prompt": "Hello, how are you?",
            "n_predict": 50,
            "temperature": 0.7
        }

        start_time = time.time()
        response = requests.post(
            f"{base_url}/completion",
            json=payload,
            timeout=30
        )
        end_time = time.time()

        if response.status_code == 200:
            data = response.json()
            content = data.get("content", "").strip()
            print(f"   Generation successful ({end_time-start_time:.1f}s)")
            print(f"   Response: {content[:100]}...")
        else:
            print(f"   Completion failed: {response.status_code}")
    except Exception as e:
        print(f"   Completion test failed: {e}")

    print("\\nTesting complete!")
    print(f"Web UI available at: {base_url}")

if __name__ == "__main__":
    test_server()
'''
    
    with open("test_api.py", 'w') as f:
        f.write(test_content)
    
    print("Created test_api.py")


def create_models_directory():
    print("Creating models directory...")
    
    os.makedirs("models", exist_ok=True)
    
    readme_content = '''# Models Directory

Place your GGUF model files here.

## Recommended Models:
- phi-4-mini-instruct-q4_k_m.gguf (Small, fast)
- llama-3.2-3b-instruct-q4_k_m.gguf (Medium)
- Any other GGUF format model

## Download Sources:
- Phi-4-mini (Q4_K_M): https://huggingface.co/matrixportalx/Phi-4-mini-instruct-Q4_K_M-GGUF
- More GGUF: https://huggingface.co/models?library=gguf

## Usage:
Update the MODEL_PATH in your startup script to match your model filename.
'''
    
    with open("models/README.md", 'w') as f:
        f.write(readme_content)
    
    print("Created models/ directory")
