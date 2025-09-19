#!/usr/bin/env python3
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

    print("\n2. Models Endpoint...")
    try:
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"   Found {len(models.get('data', []))} model(s)")
        else:
            print(f"   Models endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   Models test failed: {e}")

    print("\n3. Text Completion...")
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

    print("\nTesting complete!")
    print(f"Web UI available at: {base_url}")

if __name__ == "__main__":
    test_server()
